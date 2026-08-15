from pathlib import Path

import chromadb

from embedding_model import load_embedding_model
from text_splitter import load_all_chunks


CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "santo_pegasus_documents"


def create_vector_store():
    """Cria ou atualiza o banco vetorial com os chunks dos documentos."""

    print("Carregando modelo de embeddings...")
    model = load_embedding_model()

    print("Carregando chunks...")
    chunks = load_all_chunks()

    print(f"Total de chunks: {len(chunks)}")

    # Conecta ao ChromaDB
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Cria ou recupera a coleção
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for index, chunk in enumerate(chunks):

        # ID único para cada chunk
        chunk_id = (
            f"{chunk.metadata['document']}"
            f"-{chunk.metadata['chunk_id']}"
        )

        ids.append(chunk_id)

        # Texto do chunk
        documents.append(
            chunk.page_content
        )

        # Metadados
        metadatas.append(
            chunk.metadata
        )

        # Gera embedding
        embedding = model.encode(
            chunk.page_content
        ).tolist()

        embeddings.append(
            embedding
        )

    print("Salvando embeddings no ChromaDB...")

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("\nBanco vetorial atualizado com sucesso!")

    print(
        f"Total de chunks armazenados: "
        f"{collection.count()}"
    )


if __name__ == "__main__":
    create_vector_store()