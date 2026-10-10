"""
AIntern — ChromaDB Vector Store
Stores and retrieves company context embeddings for RAG.
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import Optional


# Use a local persistent store — data survives restarts
_client = chromadb.PersistentClient(path="./chroma_data")

# Use Groq's API for embeddings via sentence-transformers (local, free)
_ef = embedding_functions.DefaultEmbeddingFunction()


def get_collection(name: str = "company_contexts") -> chromadb.Collection:
    """Get or create a ChromaDB collection."""
    return _client.get_or_create_collection(
        name=name,
        embedding_function=_ef,
        metadata={"hnsw:space": "cosine"},
    )


def upsert_company_context(
    company_id: str,
    company_name: str,
    context_text: str,
    metadata: Optional[dict] = None,
) -> None:
    """
    Store a company's context in the vector store.
    Called when a business submits their info.
    """
    collection = get_collection()
    collection.upsert(
        ids=[company_id],
        documents=[context_text],
        metadatas=[
            {
                "company_name": company_name,
                **(metadata or {}),
            }
        ],
    )


def retrieve_similar_contexts(query: str, n_results: int = 3) -> list[str]:
    """
    Find company contexts similar to a query.
    Useful for finding reference companies during simulation generation.
    """
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count() or 1),
    )
    return results["documents"][0] if results["documents"] else []
