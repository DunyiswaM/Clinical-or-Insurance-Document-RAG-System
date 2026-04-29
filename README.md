# Clinical or Insurance Document RAG System

This project provides a RAG (Retrieval-Augmented Generation) system for processing clinical or insurance documents using LangChain and Oracle AI Vector Search.

## Features

- PDF document processing and chunking
- Embedding storage in Oracle AI Vector Search
- Health Coach prompt template for motivational SMS generation

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up Oracle Database connection (update credentials in the code).

## Usage

### Processing PDFs

Run the RAG system script:

```python
from rag_system import process_pdf_and_store_embeddings
import oracledb

# Connect to Oracle DB
connection = oracledb.connect(user="username", password="password", dsn="hostname:port/service_name")

# Process PDF
vector_store = process_pdf_and_store_embeddings("path/to/document.pdf", connection)
```

### Health Coach Prompt

Use the prompt template:

```python
from health_coach_prompt import health_coach_prompt

prompt = health_coach_prompt.format(activity_score=85, last_goal_reached="10,000 steps")
print(prompt)
```

## Troubleshooting

- Ensure Oracle Database is set up with AI Vector Search capabilities.
- Check connection credentials.
- For PDF loading issues, verify pypdf installation.
- Embeddings model may require internet for HuggingFace models.