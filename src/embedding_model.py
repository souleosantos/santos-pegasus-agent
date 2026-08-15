from sentence_transformers import SentenceTransformer


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def load_embedding_model():
    """Carrega o modelo de embeddings multilíngue."""
    return SentenceTransformer(MODEL_NAME)


def generate_embedding(model, text: str):
    """Gera o vetor de embedding para um texto."""
    return model.encode(text)


def main():
    print("Carregando modelo de embeddings...")

    model = load_embedding_model()

    text = "A Santo Pegasus utiliza uma arquitetura baseada em microsserviços."

    embedding = generate_embedding(model, text)

    print("Modelo carregado com sucesso!")
    print(f"Dimensão do vetor: {len(embedding)}")
    print(f"Primeiros valores: {embedding[:5]}")


if __name__ == "__main__":
    main()