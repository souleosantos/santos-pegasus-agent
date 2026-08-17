# 🤖 Santo Pegasus AI

Assistente virtual baseado em **RAG (Retrieval-Augmented Generation)** para consulta à documentação técnica da **Santo Pegasus Soluciones**.

O projeto permite realizar perguntas em linguagem natural sobre os documentos técnicos da empresa e obter respostas fundamentadas no conteúdo recuperado da base de conhecimento.

---

## 🎯 Descrição do Projeto

O objetivo do projeto é construir um assistente capaz de:

- consultar documentos técnicos da Santo Pegasus;
- localizar os trechos mais relevantes para uma pergunta;
- utilizar esses trechos como contexto para geração da resposta;
- responder em português do Brasil;
- apresentar as fontes recuperadas;
- evitar respostas baseadas em informações que não estejam disponíveis na documentação.

---

## 🧠 Arquitetura da Solução

O projeto utiliza uma arquitetura de **RAG (Retrieval-Augmented Generation)**.

O fluxo principal é:

```text
Pergunta do usuário
        ↓
Modelo de embeddings
        ↓
Busca por similaridade no ChromaDB
        ↓
Chunks relevantes
        ↓
Construção do contexto
        ↓
Google Gemini
        ↓
Resposta fundamentada
        ↓
Interface Streamlit
```

### Componentes

**1. Extração dos documentos**  
Os arquivos PDF armazenados em `data/raw/` são processados utilizando `pypdf`.

**2. Divisão em chunks**  
O texto extraído é dividido em pequenos trechos utilizando `RecursiveCharacterTextSplitter`, com sobreposição entre os chunks para preservar contexto.

**3. Embeddings**  
Os chunks são transformados em vetores utilizando o modelo:  
`paraphrase-multilingual-MiniLM-L12-v2`  
O modelo possui suporte multilíngue, sendo adequado para os documentos em português utilizados no projeto.

**4. Banco vetorial**  
Os embeddings são armazenados no ChromaDB, utilizando similaridade por cosseno.

**5. Recuperação**  
Quando o usuário realiza uma pergunta, ela também é transformada em embedding.  
O sistema consulta o ChromaDB e recupera os chunks mais semelhantes à pergunta.

**6. Geração da resposta**  
Os documentos recuperados são utilizados como contexto para o Google Gemini, que gera a resposta com base nesse conteúdo.

**7. Interface**  
A aplicação disponibiliza uma interface de chat construída com Streamlit, incluindo a visualização das fontes recuperadas.

---

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Google Gemini
- Google GenAI
- Sentence Transformers
- ChromaDB
- LangChain Core
- LangChain Text Splitters
- pypdf
- python-dotenv

---

## 📁 Estrutura do projeto

```text
santos-pegasus-agent/
│
├── data/
│   └── raw/
│       └── documentos PDF
│
├── src/
│   ├── app.py
│   ├── embedding_model.py
│   ├── gemini_test.py
│   ├── pdf_loader.py
│   ├── rag.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

> O diretório `chroma_db/` é criado localmente durante a execução e não deve ser versionado.

---

## ⚙️ Como Executar o Projeto

**1. Clonar o projeto**
```bash
git clone https://github.com/souleosantos/santos-pegasus-agent
cd santos-pegasus-agent
```

**2. Criar o ambiente virtual**

No Windows:
```bash
python -m venv .venv
```

Ativar o ambiente:
```powershell
.venv\Scripts\Activate.ps1
```

**3. Instalar as dependências**
```bash
pip install -r requirements.txt
```

**4. Configuração da API do Gemini**

Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_aqui
```

**5. Preparação da base vetorial**

Antes de executar o assistente, coloque seus documentos PDF na pasta `data/raw/` e execute:
```bash
python src/vector_store.py
```

**6. Executando o assistente**
```bash
streamlit run src/app.py
```
Acesse a URL: `http://localhost:8501`

---

## 🧪 Exemplos de Perguntas

Algumas perguntas que podem ser utilizadas para testar o assistente:

- Quais tecnologias fazem parte do ecossistema tecnológico principal da Santo Pegasus?
- Qual arquitetura de software a Santo Pegasus utiliza?
- Quais são os principais microsserviços da plataforma?

---

## 🤖 Exemplos das Respostas do Agente

Aqui está um exemplo de como o agente responde com base no contexto recuperado:

**Pergunta do Usuário:**  
*Quais arquiteturas de software a Santo Pegasus utiliza?*

**Resposta do Agente:**  
> Com base na documentação técnica, a Santo Pegasus utiliza primariamente uma **Arquitetura Baseada em Microsserviços**. Os serviços são divididos por domínios de negócio, permitindo escalabilidade independente e deploy contínuo. Além disso, para a comunicação entre serviços, utiliza-se arquitetura orientada a eventos (Event-Driven Architecture) através de mensageria.
> 
> *(Fontes: arquitetura_de_microsservicos_v1.pdf, engenharia_backend.pdf)*

**Pergunta do Usuário (Fora do Contexto):**  
*Qual foi o faturamento da Santo Pegasus em 2025?*

**Resposta do Agente:**  
> Não encontrei essa informação nos documentos disponíveis.

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um **Fork** do projeto.
2. Crie uma nova branch com a sua feature: `git checkout -b minha-feature`
3. Salve as suas alterações e crie um commit relatando o que você fez: `git commit -m "feat: adiciona nova funcionalidade de busca"`
4. Envie as suas alterações para o repositório remoto: `git push origin minha-feature`
5. Abra um **Pull Request**.

---

## 👨‍💻 Autor

**Leonardo Santos**