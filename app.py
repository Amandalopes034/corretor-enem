import openai
import os
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF

# Carrega chave da API do OpenAI do arquivo .env
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(page_title="Corretor ENEM com ALD", layout="wide")
st.title("📚 Corretor de Redações - ENEM com Análise Dialógica")

texto = st.text_area("✍️ Cole aqui a redação do aluno para análise completa:")

def construir_prompt(texto):
    return f"""
Você é um corretor experiente do ENEM, com domínio da matriz de competências e da Análise Linguística de Base Dialógica (ALD).

Corrija a redação a seguir com base nas 5 competências do ENEM. Para cada competência:

1. Atribua uma nota de 0 a 200.
2. Liste **detalhadamente todos os trechos que motivaram desconto de nota**, com explicações claras.
3. Explique quais critérios foram plenamente atendidos, com exemplos.
4. Justifique didaticamente o porquê da pontuação atribuída, como se explicasse a outro professor.
5. Use uma linguagem técnica e objetiva, adequada ao público docente.

Depois disso:

🔍 Faça **comentários específicos em TODOS os trechos problemáticos que ocasionaram a dminuição da nota**, incluindo:
- Qual o problema (ortografia, coerência, ambiguidade etc.);
- Qual trecho gerou o problema;
- Uma sugestão de reescrita mais adequada.

🧠 Em seguida, produza uma **Análise Dialógica Geral** nos seguintes eixos:

- **Projeto de dizer do sujeito** (intencionalidade discursiva);
- **Coerência e progressão argumentativa**;
- **Presença de vozes sociais** (autoria x discurso de outrem);
- **Relação entre texto e contexto** (sociocultural e temático).

🔽 A redação do aluno está abaixo. Faça uma correção completa e rigorosa, seguindo todas as instruções.

Redação:
\"\"\" 
{texto}
\"\"\"
"""

if st.button("🔍 Corrigir Redação") and texto:
    with st.spinner("Analisando a redação com base dialógica..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": construir_prompt(texto)}],
                temperature=0.3
            )
            correcao = response.choices[0].message.content

            st.markdown("## ✅ Resultado da Correção")
            st.write(correcao)

            # Opção para gerar PDF
            if st.button("📄 Gerar PDF com a correção"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for linha in correcao.split('\n'):
                    pdf.multi_cell(0, 10, linha)
                pdf.output("correcao_redacao.pdf")
                with open("correcao_redacao.pdf", "rb") as f:
                    st.download_button("📥 Baixar PDF da Correção", f, file_name="correcao_redacao.pdf")

        except Exception as e:
            st.error(f"Erro durante a correção: {str(e)}")
