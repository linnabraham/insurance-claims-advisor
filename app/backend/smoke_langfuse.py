"""Smoke test: verify LangFuse receives traces via LangChain callback handler.

Run from project root: python app/backend/smoke_langfuse.py
"""

import logging

from dotenv import find_dotenv, load_dotenv
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.prompts import ChatPromptTemplate
from langfuse.langchain import CallbackHandler

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    langfuse_handler = CallbackHandler()

    llm = FakeListLLM(responses=["smoke test response"])
    prompt = ChatPromptTemplate.from_template("test prompt: {input}")
    chain = prompt | llm

    response = chain.invoke(
        {"input": "langfuse connection check"},
        config={"callbacks": [langfuse_handler]},
    )

    logger.info("smoke test complete. response=%s", response)
    logger.info("check LangFuse dashboard for a new trace")


if __name__ == "__main__":
    main()
