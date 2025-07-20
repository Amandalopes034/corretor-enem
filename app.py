import openai
import os
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF

# Carrega chave da API do OpenAI do arquivo .env
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(page_title="Corretor Dialógico ENEM com ALD", layout="wide")
st.title("📚 Corretor de Redações - ENEM com Devolutiva Dialógica")

st.markdown("Esta ferramenta oferece **devolutivas formativas**, com base nas competências do ENEM e na **Análise Linguística de Base Dialógica (ALD)**. O objetivo é **promover a reflexão crítica e a reescrita consciente** da redação.")

texto = st.text_area("✍️ Cole aqui a redação do aluno para análise dialógica completa:", height=300)

def construir_prompt(texto):
    return f"""
Você é um corretor experiente do ENEM com domínio da matriz de competências e formação sólida em Análise Linguística de Base Dialógica (ALD).

Sua função é **oferecer uma devolutiva crítica, detalhada e formativa**, com base nas 5 competências do ENEM, de forma dialógica e sensível ao sujeito que escreve.

Evite dar notas. Em vez disso, oriente o aluno por meio de **perguntas, provocações e sugestões construtivas**, promovendo a **reescrita consciente e reflexiva**.

Para cada competência (C1 a C5):
- Destaque **aspectos positivos**.
- Enumere **todos os erros, inconsistências ou fragilidades**, mesmo que pequenos.
- Para cada problema, ofereça:
  - Uma **explicação clara do que está inadequado**.
  - O **trecho exato do texto**.
  - Uma **sugestão de reescrita com justificativa linguística/discursiva**.
  - Uma **pergunta provocadora** para ajudar o aluno a refletir.

No fim da análise, apresente uma **Síntese Dialógica Geral**, com base na ALD:
- Qual é o **projeto de dizer do sujeito**?
- Há coerência e progressão argumentativa?
- Quais **vozes sociais** aparecem no texto? Elas dialogam entre si?
- Que efeitos de sentido o texto produz em relação ao tema proposto?
- O que a linguagem revela sobre o posicionamento do aluno diante do tema?

Use linguagem acessível, mas crítica. Fale com o aluno como um mentor reflexivo.

Redação do aluno:
"""
{texto}
"""

if st.button("🧠 Analisar Redação com Devolutiva Dialógica") and texto:
    with st.spinner("Gerando análise crítica e dialógica da redação..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": construir_prompt(texto)}],
                temperature=0.3
            )
            devolutiva = response.choices[0].message.content

            st.markdown("## ✅ Devolutiva Dialógica da Redação")
            st.write(devolutiva)

            if st.button("📄 Gerar PDF da Devolutiva"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for linha in devolutiva.split('\n'):
                    pdf.multi_cell(0, 10, linha)
                pdf.output("devolutiva_dialógica.pdf")
                with open("devolutiva_dialógica.pdf", "rb") as f:
                    st.download_button("📥 Baixar PDF da Devolutiva", f, file_name="devolutiva_redacao_enem.pdf")

        except Exception as e:
            st.error(f"Erro durante a análise: {str(e)}")
