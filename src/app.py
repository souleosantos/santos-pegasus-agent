import streamlit as st

from rag import ask_question


# Configuração da página
st.set_page_config(
    page_title="Santo Pegasus AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Inicialização dos estados da sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Olá! Como posso ajudar você com a documentação "
                "técnica hoje?"
            ),
        }
    ]

if "latest_sources" not in st.session_state:
    st.session_state.latest_sources = []


# Cabeçalho principal
st.title("🤖 Santo Pegasus AI")

st.caption(
    "Seu assistente virtual para a documentação técnica "
    "da Santo Pegasus Soluciones. 🚀"
)


# Exibição do histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Entrada e processamento do chat
if prompt := st.chat_input(
    "Ex.: Qual arquitetura de software a Santo Pegasus utiliza?"
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(
            "Consultando a base de conhecimento..."
        ):
            try:
                answer, results = ask_question(
                    question=prompt,
                    n_results=10,
                )

                # Exibe a resposta
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                # Coleta as fontes recuperadas
                sources_data = []

                documents = results["documents"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]

                for metadata, distance in zip(
                    metadatas,
                    distances,
                ):
                    sources_data.append(
                        {
                            "document": metadata.get(
                                "document",
                                "Documento Desconhecido",
                            ),
                            "chunk_id": metadata.get(
                                "chunk_id",
                                "N/A",
                            ),
                            "distance": distance,
                        }
                    )

                st.session_state.latest_sources = sources_data

            except Exception:
                error_msg = (
                    "Ops! Não foi possível consultar a base de "
                    "conhecimento. Verifique a configuração da "
                    "aplicação e tente novamente."
                )

                st.error(error_msg)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg,
                    }
                )

                st.session_state.latest_sources = []


# Barra lateral
with st.sidebar:

    st.header("📄 Arquivos Consultados")

    st.write(
        "A última resposta foi baseada nestes documentos:"
    )

    st.divider()

    if not st.session_state.latest_sources:

        st.info(
            "Faça uma pergunta para visualizar "
            "as fontes recuperadas."
        )

    else:

        for index, source in enumerate(
            st.session_state.latest_sources,
            start=1,
        ):

            with st.container(border=True):

                st.markdown(
                    f"📑 **Fonte {index}**"
                )

                st.markdown(
                    f"**Documento:** {source['document']}"
                )

                st.markdown(
                    f"**Chunk:** {source['chunk_id']}"
                )

                st.markdown(
                    f"**Distância:** "
                    f"{source['distance']:.4f}"
                )