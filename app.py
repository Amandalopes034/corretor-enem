import openai
import os
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF

# Carrega chave da API do OpenAI do arquivo .env
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(page_title="Corretor Dialógico ENEM com ALD", layout="wide")
st.title("📚 Corretor de Redações - ENEM com Devolutiva Dialógica e Nota")

st.markdown("Esta ferramenta oferece **devolutivas formativas** com base nas competências do ENEM, na **Análise Linguística de Base Dialógica (ALD)** e agora também atribui **nota quantitativa** (0‑1000). O objetivo é **promover a reflexão crítica, a reescrita consciente e a autoavaliação numérica** da redação.")

texto = st.text_area("✍️ Cole aqui a redação do aluno para análise dialógica completa:", height=300)

def construir_prompt(texto: str) -> str:
    """Monta o prompt enviado ao modelo."""
    return f"""Você é um corretor experiente do ENEM com domínio da matriz de competências (C1 a C5) e formação sólida em Análise Linguística de Base Dialógica (ALD).

Sua função é oferecer uma devolutiva **crítica, detalhada e formativa**, de forma dialógica e sensível ao sujeito que escreve.

**IMPORTANTE**: Para cada competência (C1‑C5) você deve:
- **Destacar aspectos positivos**.
- **Enumerar e destacar TODAS** as partes do texto que apresentem erros, inconsistências, fragilidades **ou qualquer potencial de melhoria**. Não cite apenas exemplos representativos; liste cada ocorrência individual em uma lista numerada (1., 2., 3. …).
- Para cada ocorrência listada, entregue obrigatoriamente:
  1. **Trecho exato** do texto (copiado entre aspas).
  2. **Explicação** clara do que está inadequado e por quê (base linguística ou discursiva).
  3. **Sugestão de reescrita** possível, fundamentada em princípios linguísticos‑discursivos.
  4. **Pergunta crítica/reflexiva** que estimule o aluno a pensar sobre sua construção textual.

Se não houver problema em algum aspecto, justifique por que o desempenho está adequado **e** sugira como o aluno pode manter ou potencializar esse ponto forte.

### Síntese Dialógica Geral (ALD)
Após avaliar as competências, apresente uma **síntese** que contemple:
- Qual é o projeto de dizer do sujeito?
- Há coerência e progressão argumentativa?
- Quais vozes sociais aparecem no texto? Elas dialogam entre si?
- Que efeitos de sentido o texto produz em relação ao tema proposto?
- O que a linguagem revela sobre o posicionamento do aluno diante do tema?

### Nota Quantitativa
Por fim, atribua:
- **Pontuação por competência** (0‑200 cada).
- **Nota Total** (0‑1000) = soma das competências.
Justifique em até 2 linhas a pontuação de cada competência, conectando‑a aos pontos levantados na devolutiva.

Use linguagem acessível, mas crítica. Dialogue como um mentor reflexivo, interessado no crescimento da escrita do aluno.

---
Texto do aluno a ser avaliado (comece a análise a partir daqui):
""" + texto

if st.button("🧠 Analisar Redação com Devolutiva Dialógica e Nota") and texto:
    with st.spinner("Gerando análise crítica, dialógica e nota da redação..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": construir_prompt(texto)}],
                temperature=0.3,
            )
            devolutiva = response.choices[0].message.content

            st.markdown("## ✅ Devolutiva Dialógica da Redação + Nota")
            st.write(devolutiva)

            if st.button("📄 Gerar PDF da Devolutiva"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for linha in devolutiva.split("\n"):
                    pdf.multi_cell(0, 10, linha)
                pdf_path = "devolutiva_dialógica.pdf"
                pdf.output(pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Baixar PDF da Devolutiva", f, file_name="devolutiva_redacao_enem.pdf")

        except Exception as e:
            st.error(f"Erro durante a análise: {str(e)}")
