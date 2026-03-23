import chromadb
from chromadb.config import Settings

# create client
client = chromadb.Client(Settings(persist_directory="chroma_db"))

# create collection
collection = client.get_or_create_collection(name="documents")


def store_chunks(chunks, embeddings):
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids
    )


def query_chunks(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results["documents"][0]
