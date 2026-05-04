"""
Mock Oracle Database for simulating the RAG system without requiring actual Oracle DB setup.
This allows testing the entire pipeline locally.
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores.utils import DistanceStrategy

class MockOracleConnection:
    """Mock Oracle database connection for testing purposes."""

    def __init__(self, dsn: str = "mock:1521/XE"):
        self.dsn = dsn
        self.connected = True
        self.data_dir = Path("mock_db_data")
        self.data_dir.mkdir(exist_ok=True)
        print(f"Mock Oracle connection established to {dsn}")

    def close(self):
        self.connected = False
        print("Mock Oracle connection closed")

    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Mock query execution - returns sample data for testing."""
        # Simulate different query types
        if "SELECT" in query.upper() and "DOCUMENTS" in query.upper():
            return self._get_mock_documents()
        return []

    def execute_dml(self, query: str, params: Optional[Dict] = None) -> int:
        """Mock DML execution - simulates inserts/updates."""
        print(f"Mock executing DML: {query[:50]}...")
        return 1  # Return affected rows

    def _get_mock_documents(self) -> List[Dict]:
        """Return mock document data."""
        return [
            {
                "id": "doc_001",
                "text": "Patient medical record for John Doe. Diagnosis: Hypertension. Treatment: Medication prescribed.",
                "metadata": json.dumps({"patient_id": "P001", "date": "2024-01-15"})
            },
            {
                "id": "doc_002",
                "text": "Insurance claim for policy #12345. Coverage approved for outpatient services.",
                "metadata": json.dumps({"policy_id": "12345", "claim_amount": 1500.00})
            }
        ]

class MockOracleEmbeddings:
    """Mock embeddings that return fixed vectors for testing."""

    def __init__(self, conn, params=None):
        self.conn = conn
        self.params = params or {}

    def embed_query(self, text: str) -> List[float]:
        """Return a mock embedding vector."""
        # Simple mock: return a vector based on text length
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        # Create a 384-dimensional vector (similar to common embedding models)
        vector = []
        for i in range(384):
            vector.append((hash_int >> (i % 32)) % 1000 / 1000.0)
        return vector

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return mock embeddings for multiple documents."""
        return [self.embed_query(text) for text in texts]

class MockOracleVS:
    """Mock Oracle Vector Store for testing."""

    def __init__(self, connection, table_name: str, embedding_function=None, distance_strategy: DistanceStrategy = DistanceStrategy.COSINE):
        self.connection = connection
        self.table_name = table_name
        self.embedding_function = embedding_function
        self.distance_strategy = distance_strategy
        self.documents = []
        print(f"Mock OracleVS initialized for table: {table_name}")

    @classmethod
    def from_documents(cls, documents: List[Document], embedding, client, table_name: str, distance_strategy: DistanceStrategy = DistanceStrategy.COSINE):
        """Create vector store from documents."""
        instance = cls(client, table_name, embedding, distance_strategy)

        # Store documents with mock embeddings
        for i, doc in enumerate(documents):
            mock_embedding = embedding.embed_query(doc.page_content)
            instance.documents.append({
                "id": f"doc_{i+1:03d}",
                "content": doc.page_content,
                "embedding": mock_embedding,
                "metadata": doc.metadata
            })

        print(f"Mock stored {len(documents)} documents in {table_name}")
        return instance

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Mock similarity search."""
        query_embedding = self.embedding_function.embed_query(query)

        # Simple mock similarity: return first k documents
        results = []
        for doc_data in self.documents[:k]:
            results.append(Document(
                page_content=doc_data["content"],
                metadata=doc_data.get("metadata", {})
            ))

        return results

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict]] = None):
        """Add texts to the mock vector store."""
        if metadatas is None:
            metadatas = [{} for _ in texts]

        for text, metadata in zip(texts, metadatas):
            embedding = self.embedding_function.embed_query(text)
            self.documents.append({
                "id": f"doc_{len(self.documents)+1:03d}",
                "content": text,
                "embedding": embedding,
                "metadata": metadata
            })

        print(f"Mock added {len(texts)} texts to {self.table_name}")

# Monkey patch for testing
def create_mock_connection(username: str = "mock_user",
                          password: str = "mock_pass",
                          dsn: str = "localhost:1521/XE") -> MockOracleConnection:
    """Create a mock Oracle connection for testing."""
    return MockOracleConnection(dsn)

def create_mock_embeddings(conn, params=None) -> MockOracleEmbeddings:
    """Create mock embeddings for testing."""
    return MockOracleEmbeddings(conn, params)

def create_mock_vectorstore(documents: List[Document], embedding, client, table_name: str, distance_strategy: DistanceStrategy = DistanceStrategy.COSINE):
    """Create mock vector store for testing."""
    return MockOracleVS.from_documents(documents, embedding, client, table_name, distance_strategy)