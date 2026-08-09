from pathlib import Path
from pypdf import PdfReader


DATA_DIR = Path("data/raw")


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrai todo o texto disponível de um arquivo PDF."""

    reader = PdfReader(pdf_path)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


def main():
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    print(f"PDFs encontrados: {len(pdf_files)}")
    print()

    for pdf_path in pdf_files:
        text = extract_text_from_pdf(pdf_path)

        print("=" * 80)
        print(f"Arquivo: {pdf_path.name}")
        print(f"Caracteres extraídos: {len(text)}")
        print()
        print(text[:500])
        print()


if __name__ == "__main__":
    main()