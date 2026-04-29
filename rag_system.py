import oracledb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_oracledb.vectorstores import OracleVS
from langchain_core.documents import Document

def process_pdf_and_store_embeddings(pdf_path: str, connection, table_name: str = "DOCUMENTS"):
    """
    Takes a PDF document, chunks it into 500-character segments with overlap,
    and stores the embeddings in an Oracle AI Vector Search vector database.

    Args:
        pdf_path (str): Path to the PDF file.
        connection: Oracle database connection object.
        table_name (str): Name of the table to store vectors. Defaults to "DOCUMENTS".
    """
    # Load the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Chunk the text into 500-character segments with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,  # Assuming some overlap, adjust as needed
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    # Initialize embeddings (using HuggingFace for example; replace with OracleEmbeddings if preferred)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Create vector store and store embeddings
    vector_store = OracleVS.from_documents(
        chunks,
        embeddings,
        client=connection,
        table_name=table_name,
        distance_strategy="COSINE",  # or other strategies
    )

    return vector_store

# Example usage (replace with actual connection details)
if __name__ == "__main__":
    # Connection details
    username = "<username>"
    password = "<password>"
    dsn = "<hostname>:<port>/<service_name>"

    connection = oracledb.connect(user=username, password=password, dsn=dsn)

    # Process a PDF
    pdf_path = "path/to/your/document.pdf"
    vector_store = process_pdf_and_store_embeddings(pdf_path, connection)

    print("PDF processed and embeddings stored.")