from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pdf_loader import extract_text_from_pdf


DATA_DIR = Path("data/raw")


def create_chunks(pdf_path: Path) -> list[Document]:
    """Extrai o texto de um PDF e divide em chunks com metadados."""

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
        chunk_overlap=200,
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

    return chunks


def main():
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    total_chunks = 0

    for pdf_path in pdf_files:
        chunks = create_chunks(pdf_path)

        print("=" * 80)
        print(f"Arquivo: {pdf_path.name}")
        print(f"Chunks gerados: {len(chunks)}")

        print("\nPrimeiro chunk:")
        print(chunks[0].page_content[:500])

        print("\nMetadados:")
        print(chunks[0].metadata)

        print()

        total_chunks += len(chunks)

    print("=" * 80)
    print(f"Total de chunks: {total_chunks}")


if __name__ == "__main__":
    main()