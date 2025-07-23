from typing import Dict, Any
from src.retrieval import get_data

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    VectorParams
)
from langchain_ollama import OllamaEmbeddings


EMBEDDING_DIM = 1024
QDRANT_COLLECTION = "ollama-RAG"


# Qdrant client from Docker
client = QdrantClient(url="http://0.0.0.0", port=6333)
embeddings = OllamaEmbeddings(model="mxbai-embed-large") # 1024

# Create Qdrant collection if not exists
if not client.collection_exists(QDRANT_COLLECTION):
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE
        )
    )


def insert_data(data: dict):
    """Insert data in the Qdrant collection.
    args:
        data: A dictionary containing the id, text and metadata.

    returns:
        -
    """
    if not isinstance(data, dict):
        raise TypeError("The input data must be a dict.")
    
    text = data["text"]
    text_vector = embeddings.embed_query(text)
    
    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[PointStruct(
            id=data["id"],
            vector=text_vector,
            payload={
                "text": text,
                "rating": data["rating"]
            }
        )]
    )

def insert_all():
    """Get the data and insert in the qdrant collection.
    returns:
        - 
    """
    data: Dict[str, list[Any]] = get_data()
    ids, docs, metas = data["ids"], data["documents"], data["metadata"]

    for doc_id, doc, meta in zip(ids, docs, metas):
        insert_data({
            "id": doc_id,
            "text": doc,
            "rating": meta["rating"]
        })


if __name__ == "__main__":
    insert_all()
    print("\nThe data has been inserted!\n")
