import os

from dotenv import load_dotenv
from google import genai

from retriever import search_documents


load_dotenv()


MODEL_NAME = "gemini-3.6-flash"


def build_context(results):
    """Monta o contexto a partir dos documentos recuperados."""

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_parts = []

    for index, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        context_parts.append(
            f"""
--- FONTE {index} ---

Documento: {metadata["document"]}
Chunk: {metadata["chunk_id"]}
Distância: {distance:.4f}

{document}
"""
        )

    return "\n".join(context_parts)


def generate_answer(question, context):
    """Gera uma resposta utilizando exclusivamente o contexto recuperado."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY não encontrada no arquivo .env"
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
Você é o assistente de conhecimento interno da Santo Pegasus Soluciones.

Sua função é responder perguntas utilizando EXCLUSIVAMENTE
as informações presentes no CONTEXTO fornecido.

REGRAS IMPORTANTES:

1. Não invente informações.
2. Não utilize conhecimento externo ao contexto.
3. Se a informação não estiver presente no contexto, responda:
   "Não encontrei essa informação nos documentos disponíveis."
4. Responda em português do Brasil.
5. Seja claro, objetivo e organizado.
6. Quando a pergunta pedir uma lista, organize a resposta em tópicos.
7. Sempre informe o documento utilizado como fonte.
8. Não mencione que você é um modelo de linguagem.
9. Não faça suposições além do que está escrito no contexto.
10. Se diferentes fontes apresentarem informações diferentes,
    apresente a diferença em vez de inventar uma conclusão.

CONTEXTO:

{context}

PERGUNTA:

{question}

RESPONDA:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text


def ask_question(question: str, n_results: int = 5):
    """
    Executa o pipeline completo do RAG:

    pergunta
        ↓
    recuperação dos documentos
        ↓
    construção do contexto
        ↓
    geração da resposta
    """

    results = search_documents(
        query=question,
        n_results=n_results,
    )

    print("\n" + "=" * 80)
    print("DEBUG - DOCUMENTOS RECUPERADOS")
    print("=" * 80)

    for index, (document, metadata, distance) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ),
        start=1,
    ):
        print(f"\nResultado {index}")
        print(f"Documento: {metadata['document']}")
        print(f"Chunk: {metadata['chunk_id']}")
        print(f"Distância: {distance:.4f}")

    context = build_context(results)

    answer = generate_answer(
        question,
        context,
    )

    return answer, results

def main():
    question = input("Digite sua pergunta: ")

    print("\nBuscando informações relevantes...")

    answer, results = ask_question(
        question,
        n_results=10,
    )

    print("\n" + "=" * 80)
    print("RESPOSTA DO AGENTE")
    print("=" * 80)

    print(answer)

    print("\n" + "=" * 80)
    print("FONTES RECUPERADAS")
    print("=" * 80)

    for index, metadata in enumerate(
        results["metadatas"][0],
        start=1,
    ):
        print(
            f"{index}. "
            f"{metadata['document']} "
            f"(chunk {metadata['chunk_id']})"
        )


if __name__ == "__main__":
    main()