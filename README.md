# Claims Advisor — AI-Powered Insurance Claims Triage and Decision Support

An intelligent decision-support tool for insurance claims adjusters. Upload a claim document and a policy document, and receive a structured assessment — claim summary, relevant policy clauses, coverage determination, fraud signals, and a recommended action — all in seconds.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/linnabraham/insurance-claims-advisor.git
cd insurance-claims-advisor

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Open .env and fill in your actual values (see Environment Variables below)

# Start the FastAPI backend
python -m backend.run

# In a separate terminal, start the Streamlit frontend
streamlit run frontend/app.py
```

---

## Environment Variables

Copy `.env.example` to `.env` and populate each value. **Never commit `.env` to version control.**

| Variable | Description |
|---|---|
| `BACKEND_HOST` | Host address the FastAPI server binds to (default: 0.0.0.0) |
| `BACKEND_PORT` | Port the FastAPI server listens on (default: 8000) |
| `BACKEND_URL`  | Base URL the Streamlit frontend uses to reach the backend (default: http://localhost:8000) |


---

## Project Structure

```
insurance-claims-advisor/
├── backend/
│   ├── main.py              # FastAPI application entry point
├── frontend/
│   └── app.py               # Streamlit application
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```
