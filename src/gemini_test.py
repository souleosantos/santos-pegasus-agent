import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def main():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY não encontrada no arquivo .env"
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Responda apenas: Gemini funcionando!",
    )

    print("Resposta do Gemini:")
    print(response.text)


if __name__ == "__main__":
    main()