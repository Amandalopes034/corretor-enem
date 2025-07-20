import os
import openai
import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Corretor de Redações - ENEM com Análise Dialógica", layout="wide")
st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")
st.markdown("Cole sua redação abaixo e receba uma **avaliação técnica detalhada**, voltada para professores:")

texto = st.text_area("📌 Redação do aluno:", height=300)
gerar_pdf = False
resultado = ""

prompt = f"""
Você é um corretor experiente e detalhista, com domínio das 5 competências do ENEM. Seu público são professores de redação.

Tarefa:
Avalie tecnicamente a redação abaixo, justificando cada ponto de forma pedagógica e específica, como um professor corrigindo para outro professor.

Instruções:
1. Para cada competência (C1 a C5), forneça:
   - Nota (0–200)
   - Justificativa técnica completa e didática
   - Lista de **todos os aspectos positivos e negativos observados**
   - Citações concretas da redação como evidência da nota

2. Ao final, escreva uma síntese geral da redação, destacando:
   - Projeto de dizer do sujeito
   - Coesão textual
   - Presença de vozes sociais
   - Relação com o tema e os textos motivadores

Redação:
\"\"\"
{texto}
\"\"\"
"""

def gerar_pdf_saida(conteudo, nome_arquivo="correcao_redacao.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linha in conteudo.split("\n"):
        pdf.multi_cell(0, 10, linha)
    pdf.output(nome_arquivo)
    return nome_arquivo

if st.button("Corrigir Redação"):
    if not texto.strip():
        st.warning("Por favor, cole a redação antes de corrigir.")
    else:
        with st.spinner("Corrigindo a redação..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é um corretor especialista do ENEM."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    max_tokens=2200
                )
                resultado = response.choices[0].message.content
                st.markdown("## 📋 Comentários detalhados da correção:")
                st.markdown(resultado)
                gerar_pdf = True
            except Exception as e:
                st.error(f"Erro ao acessar a API da OpenAI: {e}")

if gerar_pdf and resultado:
    if st.button("📄 Gerar PDF da correção"):
        nome_pdf = gerar_pdf_saida(resultado)
        with open(nome_pdf, "rb") as f:
            st.download_button(
                label="📥 Clique para baixar a correção em PDF",
                data=f,
                file_name=nome_pdf,
                mime="application/pdf"
            )
