import oracledb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_oracledb.embeddings import OracleEmbeddings
from langchain_oracledb.vectorstores import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
import os
import sys

def process_pdf_and_store_embeddings(pdf_path: str, connection, table_name: str = "DOCUMENTS", use_mock: bool = False):
    """
    Takes a PDF document, chunks it into 500-character segments with overlap,
    and stores the embeddings in an Oracle AI Vector Search vector database.

    Args:
        pdf_path (str): Path to the PDF file.
        connection: Oracle database connection object.
        table_name (str): Name of the table to store vectors. Defaults to "DOCUMENTS".
        use_mock (bool): Whether to use mock embeddings instead of Oracle embeddings.

    Returns:
        vector_store: The created vector store object.
    """
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Load the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError(f"No content found in PDF: {pdf_path}")

    # Chunk the text into 500-character segments with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,  # Assuming some overlap, adjust as needed
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    if use_mock:
        # Use mock embeddings for testing
        from mock_database import MockOracleEmbeddings
        embeddings = MockOracleEmbeddings(connection)
    else:
        # Use Oracle AI embeddings
        embeddings = OracleEmbeddings(conn=connection, params={"provider": "database", "model": "DB_MODEL"})

    # Create vector store and store embeddings
    if use_mock:
        from mock_database import MockOracleVS
        vector_store = MockOracleVS.from_documents(
            chunks,
            embeddings,
            client=connection,
            table_name=table_name,
            distance_strategy=DistanceStrategy.COSINE,
        )
    else:
        vector_store = OracleVS.from_documents(
            chunks,
            embeddings,
            client=connection,
            table_name=table_name,
            distance_strategy=DistanceStrategy.COSINE,
        )

    return vector_store

# Example usage (replace with actual connection details)
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process PDF documents for RAG system')
    parser.add_argument('--pdf', type=str, help='Path to PDF file to process')
    parser.add_argument('--mock', action='store_true', help='Use mock database for testing')
    parser.add_argument('--table', type=str, default='DOCUMENTS', help='Table name for vector storage')

    args = parser.parse_args()

    try:
        if args.mock:
            # Use mock database for testing
            from mock_database import MockOracleConnection
            print("Using mock database for testing...")
            connection = MockOracleConnection()
            use_mock = True
        else:
            # Use real Oracle database
            print("Using real Oracle database...")
            # Connection details - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
            username = "<username>"
            password = "<password>"
            dsn = "<hostname>:<port>/<service_name>"

            if username == "<username>" or password == "<password>" or dsn == "<hostname>:<port>/<service_name>":
                print("ERROR: Please update the connection credentials in rag_system.py with your actual Oracle database details.")
                print("For testing, use the --mock flag: python rag_system.py --mock --pdf path/to/document.pdf")
                sys.exit(1)

            connection = oracledb.connect(user=username, password=password, dsn=dsn)
            use_mock = False

        # Determine PDF path
        if args.pdf:
            pdf_path = args.pdf
        else:
            # Try to use sample PDFs if they exist
            sample_pdf = "sample_clinical_document.pdf"
            if os.path.exists(sample_pdf):
                pdf_path = sample_pdf
                print(f"Using sample PDF: {sample_pdf}")
            else:
                print("ERROR: No PDF file specified. Use --pdf to specify a PDF file, or generate sample PDFs with: python create_sample_pdfs.py")
                sys.exit(1)

        # Process the PDF
        vector_store = process_pdf_and_store_embeddings(pdf_path, connection, args.table, use_mock)

        print(f"✅ PDF processed and embeddings stored in table '{args.table}'!")

        # Close connection
        if hasattr(connection, 'close'):
            connection.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)