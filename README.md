
# RAG-APP

A basic Retrieval-Augmented Generation (RAG) application built with FastAPI.

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```
APP_NAME="RAG-APP"
APP_ENV=local
```

### Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Project Structure

```
RAG-App/
├── .env
├── requirements.txt
├── main.py
└── README.md
```

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server
