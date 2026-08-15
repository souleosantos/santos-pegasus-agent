from pathlib import Path

import chromadb

from embedding_model import load_embedding_model


CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "santo_pegasus_documents"


_model = None
_collection = None


def get_model():
    """Carrega o modelo de embeddings uma única vez."""

    global _model

    if _model is None:
        print("Carregando modelo de embeddings...")
        _model = load_embedding_model()

    return _model


def get_collection():
    """Conecta à coleção do ChromaDB uma única vez."""

    global _collection

    if _collection is None:
        client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        _collection = client.get_collection(
            name=COLLECTION_NAME
        )

    return _collection


def search_documents(
    query: str,
    n_results: int = 5,
):
    """
    Busca os chunks mais relevantes para uma pergunta.

    Parâmetros:
        query: pergunta realizada pelo usuário.
        n_results: quantidade de chunks recuperados.

    Retorna:
        Resultado da consulta do ChromaDB.
    """

    if not query or not query.strip():
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    model = get_model()
    collection = get_collection()

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    return results


def main():
    """Executa uma busca pelo terminal."""

    query = input(
        "Digite sua pergunta: "
    ).strip()

    results = search_documents(
        query,
        n_results=10,
    )

    print("\n" + "=" * 80)
    print("RESULTADOS DA BUSCA")
    print("=" * 80)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, (
        document,
        metadata,
        distance,
    ) in enumerate(
        zip(
            documents,
            metadatas,
            distances,
        ),
        start=1,
    ):

        print(
            f"\nResultado {index}"
        )

        print("-" * 80)

        print(
            f"Documento: "
            f"{metadata['document']}"
        )

        print(
            f"Chunk: "
            f"{metadata['chunk_id']}"
        )

        print(
            f"Distância: "
            f"{distance:.4f}"
        )

        print("\nTexto:")

        print(
            document[:1500]
        )


if __name__ == "__main__":
    main()