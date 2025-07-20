import streamlit as st
import openai
import os
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Corretor de Redações - ENEM com Análise Dialógica")
st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

st.markdown("""
Este corretor utiliza inteligência artificial para avaliar redações do ENEM com base nos critérios oficiais e fundamentação na análise dialógica da linguagem, conforme Bakhtin e o Círculo. A correção é criteriosa, considerando a interação entre vozes sociais, argumentação responsiva e o projeto de dizer do sujeito.
""")

texto = st.text_area("Cole sua redação aqui:", height=300)

if st.button("Corrigir Redação") and texto:
    prompt = f"""
Você é um corretor experiente de redações do ENEM, formado em Letras, especializado em Análise Dialógica da linguagem (Bakhtin e o Círculo) e nos critérios oficiais do ENEM.

Corrija a redação abaixo com base nas 5 competências do ENEM (de 0 a 200 pontos cada).

Para cada competência, forneça:
- Nota objetiva (0 a 200)
- Justificativa analítica com trechos da redação que embasem a nota
- Comentários linguísticos detalhados (norma padrão, ortografia, concordância, grafia de nomes próprios etc.)
- Interpretação dialógica: aponte vozes sociais presentes, projeto de dizer, relação entre texto e contexto, uso de autores
- Na competência 5, verifique a presença dos 5 elementos: agente, ação, meio, finalidade e detalhamento

Redação:
"""{texto}"""
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um corretor do ENEM especializado em análise dialógica da linguagem."},
                {"role": "user", "content": prompt}
            ]
        )
        resposta = response.choices[0].message.content
        st.markdown("### Resultado da Correção:")
        st.markdown(resposta)

        # Gerar PDF da correção
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for linha in resposta.split('\n'):
            pdf.multi_cell(0, 10, linha)
        pdf_path = "/tmp/correcao_redacao.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Baixar correção em PDF",
                data=f,
                file_name="correcao_redacao.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Erro ao acessar a API da OpenAI: {e}")
