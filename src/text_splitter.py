from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pdf_loader import extract_text_from_pdf


DATA_DIR = Path("data/raw")


def create_chunks(pdf_path: Path) -> list[Document]:
    """Extrai o texto de um PDF e divide em chunks preservando contexto."""

    text = extract_text_from_pdf(pdf_path)

    document = Document(
        page_content=text,
        metadata={
            "source": str(pdf_path),
            "document": pdf_path.stem,
        },
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=250,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents([document])

    for chunk_id, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = chunk_id

        # Adiciona o nome do documento ao próprio texto.
        # Isso fornece contexto adicional para o modelo de embedding.
        chunk.page_content = (
            f"Documento: {pdf_path.stem}\n\n"
            f"{chunk.page_content}"
        )

    return chunks


def load_all_chunks() -> list[Document]:
    """Carrega e divide todos os PDFs da pasta data/raw."""

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    all_chunks = []

    for pdf_path in pdf_files:
        chunks = create_chunks(pdf_path)
        all_chunks.extend(chunks)

    return all_chunks


def main():
    chunks = load_all_chunks()

    print(f"Total de chunks: {len(chunks)}")

    print("\nExemplo de chunk:")
    print(chunks[0].page_content[:500])

    print("\nMetadados:")
    print(chunks[0].metadata)


if __name__ == "__main__":
    main()