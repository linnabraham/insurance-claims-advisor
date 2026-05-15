"""Embedding + retrieval layer backed by ChromaDB.

Indexes chunks emitted by the policy_ingestion pipeline (a list of
``{section, text}`` dicts) into a persistent Chroma collection, and
exposes a retrieve() function to query the collection for top-k matches.

CLI usage:

    python -m backend.document_processor index <chunks.json> \\
        --doc-id pci-motor-faq --collection policies

    python -m backend.document_processor query "<text>" \\
        --collection policies --top-k 5
"""

import argparse
import json
import logging
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from backend.config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

_embedding_model: SentenceTransformer | None = None
_chroma_client: chromadb.ClientAPI | None = None


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        logger.info("Loading embedding model %s", EMBEDDING_MODEL_NAME)
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


def get_chroma_client() -> chromadb.ClientAPI:
    global _chroma_client
    if _chroma_client is None:
        CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
        logger.info("ChromaDB client initialised at %s", CHROMA_PERSIST_DIR)
    return _chroma_client


def embed_and_store(chunks: list[dict], doc_id: str, collection_name: str) -> int:
    """Embed chunks and store them in a ChromaDB collection.

    Args:
        chunks: List of ``{section, text}`` dicts (as produced by the
            policy_ingestion pipeline / chunks.json). Entries with empty or
            whitespace-only ``text`` are skipped with a warning.
        doc_id: Unique identifier for the source document. Used as the
            metadata field and as the prefix for chunk IDs.
        collection_name: Target ChromaDB collection (e.g. 'policies' or 'claims').

    Returns:
        Number of chunks actually stored (after skipping empty ones).
    """
    if not chunks:
        logger.warning("embed_and_store: empty chunk list for doc_id=%s", doc_id)
        return 0

    texts: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    for i, chunk in enumerate(chunks):
        text = (chunk.get("text") or "").strip()
        if not text:
            logger.warning("Skipping chunk %d (empty text) for doc_id=%s", i, doc_id)
            continue
        texts.append(text)
        metadatas.append(
            {
                "doc_id": doc_id,
                "chunk_index": i,
                "section": chunk.get("section", ""),
            }
        )
        ids.append(f"{doc_id}::chunk_{i}")

    if not texts:
        logger.warning("embed_and_store: all chunks were empty for doc_id=%s", doc_id)
        return 0

    model = get_embedding_model()
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )

    logger.info(
        "Stored %d chunks in collection '%s' for doc_id=%s",
        len(texts),
        collection_name,
        doc_id,
    )
    return len(texts)


def retrieve(query: str, collection_name: str, top_k: int = 5) -> list[dict]:
    """Embed a query and return the top-k matching chunks.

    Returns a list of dicts with keys: text, section, doc_id, chunk_index, distance.
    """
    model = get_embedding_model()
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    query_embedding = model.encode([query], show_progress_bar=False).tolist()
    result = collection.query(query_embeddings=query_embedding, n_results=top_k)

    hits: list[dict] = []
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    for text, meta, dist in zip(documents, metadatas, distances):
        hits.append(
            {
                "text": text,
                "section": meta.get("section", ""),
                "doc_id": meta.get("doc_id", ""),
                "chunk_index": meta.get("chunk_index"),
                "distance": dist,
            }
        )
    return hits


def _load_chunks(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a JSON list of chunk objects")
    return data


def _cmd_index(args: argparse.Namespace) -> None:
    chunks_path = Path(args.chunks)
    doc_id = args.doc_id or chunks_path.stem
    chunks = _load_chunks(chunks_path)
    n = embed_and_store(chunks, doc_id=doc_id, collection_name=args.collection)
    print(f"Indexed {n} chunks into collection '{args.collection}' (doc_id={doc_id})")


def _cmd_query(args: argparse.Namespace) -> None:
    hits = retrieve(args.query, collection_name=args.collection, top_k=args.top_k)
    if not hits:
        print("No hits.")
        return
    for rank, hit in enumerate(hits, 1):
        preview = hit["text"].replace("\n", " ")
        if len(preview) > 200:
            preview = preview[:200] + "..."
        print(
            f"#{rank}  distance={hit['distance']:.4f}  "
            f"section={hit['section']!r}  doc_id={hit['doc_id']}  "
            f"chunk_index={hit['chunk_index']}"
        )
        print(f"     {preview}\n")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )

    parser = argparse.ArgumentParser(
        description="Index chunked policy text into ChromaDB and query it."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="Embed and store a chunks JSON file.")
    p_index.add_argument(
        "chunks", help="Path to a chunks JSON file (list of {section, text})."
    )
    p_index.add_argument(
        "--doc-id",
        default=None,
        help="Document identifier (defaults to the chunks file stem).",
    )
    p_index.add_argument(
        "--collection", default="policies", help="Target Chroma collection."
    )
    p_index.set_defaults(func=_cmd_index)

    p_query = sub.add_parser("query", help="Query the collection for top-k matches.")
    p_query.add_argument("query", help="Query text.")
    p_query.add_argument(
        "--collection", default="policies", help="Chroma collection to query."
    )
    p_query.add_argument(
        "--top-k", type=int, default=5, help="Number of hits to return."
    )
    p_query.set_defaults(func=_cmd_query)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
