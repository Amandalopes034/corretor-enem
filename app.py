import openai
import os
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

texto = st.text_area("Cole sua redação aqui:")

if st.button("Corrigir Redação") and texto:
    with st.spinner("Analisando a redação..."):

        prompt = f"""
Você é um corretor experiente do ENEM com profundo domínio da Análise Linguística de Base Dialógica (ALD). Avalie a redação abaixo conforme os critérios C1 a C5:

C1: Norma padrão (nota de 0 a 200)  
C2: Compreensão da proposta (nota de 0 a 200)  
C3: Organização dos argumentos (nota de 0 a 200)  
C4: Coesão textual (nota de 0 a 200)  
C5: Proposta de intervenção (nota de 0 a 200)  

Para cada critério:
- Atribua uma nota objetiva.
- Liste detalhadamente os pontos observados que justificam a nota.
- Mencione trechos que colaboraram ou comprometeram a pontuação.

Depois, forneça:
- Comentários por trechos problemáticos com sugestão de reescrita.
- Uma análise dialógica geral considerando:
  - Projeto de dizer do sujeito;
  - Coerência e progressão argumentativa;
  - Presença de vozes sociais;
  - Relação entre texto e contexto.

Redação do aluno:
\"\"\"
{texto}
\"\"\"
"""

        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            correcao = resposta.choices[0].message.content
            st.markdown("## 📄 Resultado da Correção")
            st.write(correcao)

            # Gerar PDF
            gerar_pdf = st.button("📥 Baixar correção em PDF")
            if gerar_pdf:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for linha in correcao.split('\n'):
                    pdf.multi_cell(0, 10, linha)
                pdf.output("correcao_redacao.pdf")
                with open("correcao_redacao.pdf", "rb") as f:
                    st.download_button("📩 Clique para baixar", f, file_name="correcao_redacao.pdf")

        except Exception as e:
            st.error(f"Ocorreu um erro durante a correção: {str(e)}")
