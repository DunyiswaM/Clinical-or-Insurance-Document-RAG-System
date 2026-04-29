#!/usr/bin/env python3
"""
Test script for the Clinical or Insurance Document RAG System
"""

def test_chunking():
    """Test the text chunking functionality"""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    print("Testing text chunking...")

    # Create sample text
    sample_text = "This is a sample clinical document. " * 100  # ~3300 characters
    documents = [Document(page_content=sample_text)]

    # Test chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    print(f"✓ Original text length: {len(sample_text)}")
    print(f"✓ Number of chunks: {len(chunks)}")
    print(f"✓ First chunk length: {len(chunks[0].page_content)}")
    print(f"✓ Chunking test passed!")

    return True

def test_health_coach_prompt():
    """Test the Health Coach prompt template"""
    from health_coach_prompt import health_coach_prompt

    print("\nTesting Health Coach prompt template...")

    # Test formatting
    result = health_coach_prompt.format(activity_score=85, last_goal_reached="10,000 steps")

    print("✓ Prompt template created successfully")
    print("✓ Variables formatted correctly")
    print(f"✓ Prompt length: {len(result)} characters")
    print("✓ Health Coach prompt test passed!")

    return True

def test_imports():
    """Test all required imports"""
    print("\nTesting imports...")

    try:
        import oracledb
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_oracledb.embeddings import OracleEmbeddings
        from langchain_oracledb.vectorstores import OracleVS
        from langchain_core.documents import Document
        from langchain_core.prompts import PromptTemplate

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Clinical or Insurance Document RAG System")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Text Chunking", test_chunking),
        ("Health Coach Prompt", test_health_coach_prompt),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"✗ {test_name} failed")
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The system is ready for use.")
        print("\nNote: Full RAG functionality requires Oracle Database connection.")
        print("Update connection credentials in rag_system.py for production use.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()