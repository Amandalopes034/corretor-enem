import streamlit as st
import openai
import os

# Título do app
st.set_page_config(page_title="Corretor ENEM com Análise Dialógica", layout="wide")
st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

# Coleta a chave secreta da OpenAI (armazenada nos secrets do Streamlit Cloud)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Campo para colar a redação
st.markdown("### Cole sua redação abaixo:")
texto = st.text_area("Redação", height=300)

# Botão de envio
if st.button("Corrigir Redação"):
    if not texto.strip():
        st.warning("Por favor, cole uma redação antes de enviar.")
    else:
        with st.spinner("Corrigindo..."):

            prompt = f"""
Você é um corretor especializado em redações do ENEM. Avalie o texto a seguir com dois objetivos:

1. Faça comentários por trechos, destacando partes do texto que apresentem problemas de coesão, argumentação, estrutura, inadequações gramaticais ou desvios do projeto de dizer do autor. Use destaques **negrito** nos trechos e faça comentários explicativos abaixo de cada trecho problemático.
2. Ao final, forneça uma nota para cada uma das 5 competências do ENEM (de 0 a 200), seguidas da nota final (soma das 5).

Redação:
\"\"\"{texto}\"\"\"

Formato de saída:
- Comentários por trechos com marcação clara (**trecho**) e explicação
- Tabela com notas das 5 competências + nota final
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1200
                )

                resultado = response.choices[0].message.content
                st.markdown("### ✅ Resultado da Correção:")
                st.markdown(resultado)

            except Exception as e:
                st.error(f"Erro ao acessar a API da OpenAI: {e}")
