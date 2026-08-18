FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Instala PyTorch somente para CPU
RUN pip install --no-cache-dir \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

# Instala as demais dependências
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
COPY chroma_db ./chroma_db

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]