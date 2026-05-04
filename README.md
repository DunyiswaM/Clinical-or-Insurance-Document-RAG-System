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

## Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

This will validate:
- All required imports
- Text chunking functionality
- Health Coach prompt template

## Simulation

Run the complete system simulation with mock database:

```bash
python simulate_rag_system.py
```

This demonstrates:
- PDF document creation and processing
- Mock Oracle database operations
- Text chunking and embedding storage
- Vector similarity search
- Health Coach prompt generation

Run individual component tests:

```bash
python simulate_rag_system.py --test
```

## Sample Documents

The system includes sample clinical and insurance documents:
- `sample_clinical_document.pdf` - Complete medical record
- `sample_insurance_document.pdf` - Insurance claim document

Generate new sample documents:

```bash
python create_sample_pdfs.py
```

## Usage

### Processing PDFs with Mock Database (Testing)

For testing without a real Oracle database:

```bash
# Generate sample PDFs first
python create_sample_pdfs.py

# Process a PDF using mock database
python rag_system.py --mock --pdf sample_clinical_document.pdf

# Or process insurance document
python rag_system.py --mock --pdf sample_insurance_document.pdf
```

### Processing PDFs with Real Oracle Database (Production)

For production use with actual Oracle AI Vector Search:

1. Update connection credentials in `rag_system.py`
2. Run the system:

```bash
python rag_system.py --pdf path/to/your/document.pdf
```

### Command Line Options

- `--pdf PATH`: Path to PDF file to process
- `--mock`: Use mock database for testing (no real Oracle DB required)
- `--table NAME`: Table name for vector storage (default: DOCUMENTS)

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