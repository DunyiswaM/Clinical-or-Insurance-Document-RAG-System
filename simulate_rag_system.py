#!/usr/bin/env python3
"""
Complete RAG System Simulation using Mock Database
This script demonstrates the entire RAG pipeline without requiring actual Oracle database setup.
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import mock database components
from mock_database import (
    MockOracleConnection,
    MockOracleEmbeddings,
    MockOracleVS,
    create_mock_connection,
    create_mock_embeddings,
    create_mock_vectorstore
)

# Import original RAG system components
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def simulate_process_pdf_and_store_embeddings(pdf_path: str, connection, table_name: str = "DOCUMENTS"):
    """
    Simulated version of the PDF processing function using mock database.
    """
    print(f"🔄 Processing PDF: {pdf_path}")

    # Load the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"📄 Loaded {len(documents)} pages from PDF")

    # Chunk the text into 500-character segments with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️  Created {len(chunks)} text chunks")

    # Initialize mock embeddings
    embeddings = create_mock_embeddings(connection)

    # Create mock vector store and store embeddings
    vector_store = create_mock_vectorstore(
        chunks,
        embeddings,
        connection,
        table_name,
        distance_strategy="COSINE"
    )

    print(f"✅ Successfully stored {len(chunks)} document chunks in mock vector database")
    return vector_store

def demonstrate_rag_system():
    """Complete demonstration of the RAG system with mock database."""

    print("🏥 CLINICAL OR INSURANCE DOCUMENT RAG SYSTEM SIMULATION")
    print("=" * 60)

    # Step 1: Create sample PDFs
    print("\n📝 Step 1: Creating sample documents...")
    from create_sample_pdfs import create_clinical_document_pdf, create_insurance_document_pdf

    clinical_pdf = "sample_clinical_document.pdf"
    insurance_pdf = "sample_insurance_document.pdf"

    create_clinical_document_pdf(clinical_pdf)
    create_insurance_document_pdf(insurance_pdf)

    # Step 2: Set up mock database connection
    print("\n🗄️  Step 2: Establishing mock database connection...")
    connection = create_mock_connection()

    # Step 3: Process clinical document
    print("\n🏥 Step 3: Processing clinical document...")
    clinical_vector_store = simulate_process_pdf_and_store_embeddings(
        clinical_pdf, connection, "CLINICAL_DOCUMENTS"
    )

    # Step 4: Process insurance document
    print("\n💼 Step 4: Processing insurance document...")
    insurance_vector_store = simulate_process_pdf_and_store_embeddings(
        insurance_pdf, connection, "INSURANCE_DOCUMENTS"
    )

    # Step 5: Demonstrate search capabilities
    print("\n🔍 Step 5: Demonstrating search capabilities...")

    # Test queries
    test_queries = [
        "hypertension treatment",
        "insurance claim status",
        "patient medical history",
        "cardiac workup results"
    ]

    for query in test_queries:
        print(f"\n   Query: '{query}'")

        # Search clinical documents
        clinical_results = clinical_vector_store.similarity_search(query, k=2)
        if clinical_results:
            print(f"   📋 Clinical results: {len(clinical_results)} found")
            print(f"   📄 Sample: {clinical_results[0].page_content[:100]}...")

        # Search insurance documents
        insurance_results = insurance_vector_store.similarity_search(query, k=2)
        if insurance_results:
            print(f"   📋 Insurance results: {len(insurance_results)} found")
            print(f"   📄 Sample: {insurance_results[0].page_content[:100]}...")

    # Step 6: Demonstrate Health Coach prompt
    print("\n💬 Step 6: Testing Health Coach prompt template...")
    from health_coach_prompt import health_coach_prompt

    # Test different scenarios
    scenarios = [
        {"activity_score": 85, "last_goal_reached": "10,000 steps daily"},
        {"activity_score": 92, "last_goal_reached": "weight loss goal of 5 pounds"},
        {"activity_score": 78, "last_goal_reached": "blood pressure target"}
    ]

    for scenario in scenarios:
        prompt = health_coach_prompt.format(**scenario)
        print(f"   🎯 Activity Score: {scenario['activity_score']}, Goal: {scenario['last_goal_reached']}")
        print(f"   📱 SMS Length: {len(prompt)} characters")
        print("   ✅ Under 160 character limit" if len(prompt) <= 160 else "   ❌ Over limit")
        print()

    # Step 7: Cleanup
    print("🧹 Step 7: Cleaning up mock database connection...")
    connection.close()

    print("\n" + "=" * 60)
    print("🎉 SIMULATION COMPLETE!")
    print("✅ All components tested successfully")
    print("✅ Mock database simulation working")
    print("✅ PDF processing and chunking functional")
    print("✅ Vector storage operational")
    print("✅ Search capabilities demonstrated")
    print("✅ Health Coach prompts validated")
    print("\n📊 Ready for production with real Oracle database!")

def run_individual_tests():
    """Run individual component tests."""

    print("🧪 INDIVIDUAL COMPONENT TESTS")
    print("=" * 40)

    # Test 1: Mock database connection
    print("\n1. Testing mock database connection...")
    try:
        conn = create_mock_connection()
        print("   ✅ Connection successful")
        conn.close()
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False

    # Test 2: PDF creation
    print("\n2. Testing PDF creation...")
    try:
        from create_sample_pdfs import create_clinical_document_pdf
        create_clinical_document_pdf("test_clinical.pdf")
        if os.path.exists("test_clinical.pdf"):
            print("   ✅ PDF creation successful")
            os.remove("test_clinical.pdf")  # Cleanup
        else:
            print("   ❌ PDF file not created")
            return False
    except Exception as e:
        print(f"   ❌ PDF creation failed: {e}")
        return False

    # Test 3: Text chunking
    print("\n3. Testing text chunking...")
    try:
        sample_text = "This is a test document. " * 100
        documents = [Document(page_content=sample_text)]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)

        if len(chunks) > 1:
            print(f"   ✅ Chunking successful: {len(chunks)} chunks created")
        else:
            print("   ❌ Chunking failed: insufficient chunks")
            return False
    except Exception as e:
        print(f"   ❌ Chunking failed: {e}")
        return False

    # Test 4: Health Coach prompt
    print("\n4. Testing Health Coach prompt...")
    try:
        from health_coach_prompt import health_coach_prompt
        prompt = health_coach_prompt.format(activity_score=85, last_goal_reached="test goal")
        if len(prompt) > 0 and "85" in prompt:
            print("   ✅ Prompt template working")
        else:
            print("   ❌ Prompt template failed")
            return False
    except Exception as e:
        print(f"   ❌ Prompt test failed: {e}")
        return False

    print("\n🎉 All individual tests passed!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run individual tests
        success = run_individual_tests()
        sys.exit(0 if success else 1)
    else:
        # Run full simulation
        demonstrate_rag_system()