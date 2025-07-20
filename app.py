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

texto = st.text_area("✍️ Cole aqui a redação do aluno para análise completa:", height=300)

def construir_prompt(texto):
    return f"""
Você é um corretor experiente do ENEM, com domínio da matriz de competências e da Análise Linguística de Base Dialógica (ALD).

Corrija a redação a seguir com base nas 5 competências do ENEM. Utilize os critérios abaixo (baseados na cartilha oficial do INEP) e lembre-se:

⚠️ Elenque **todos os erros e inconsistências** encontrados em cada competência, mas **considere que até 2 erros pontuais não justificam desconto na nota**, a menos que comprometam gravemente a compreensão do texto.

**Competência 1: Norma padrão da língua escrita**
- Avalie ortografia, acentuação, pontuação, concordância, regência, crase, tempos verbais e construção sintática.
- Penalize reincidência ou erros que dificultem a leitura. Desconsidere até 2 erros pontuais se não interferirem no entendimento.

**Competência 2: Compreensão da proposta de redação**
- Verifique se o texto atende integralmente ao tema e à proposta dissertativo-argumentativa.
- Penalize tangenciamento ou fuga parcial. Avalie o uso produtivo dos textos motivadores.

**Competência 3: Seleção e organização de argumentos**
- Avalie a construção da tese, progressão lógica, articulação de ideias, repertório e profundidade.

**Competência 4: Coesão textual**
- Avalie conectivos, coesão referencial, sequencial e lexical. Verifique fluidez e uso adequado de mecanismos coesivos.

**Competência 5: Proposta de intervenção**
- A proposta deve apresentar: agente, ação, meio/modo, finalidade e detalhamento. Penalize propostas vagas ou sem conexão com o problema abordado.

**Para cada competência (C1 a C5):**
1. Informe a nota objetiva (0–200)
2. Explique os critérios aplicados
3. Liste os pontos positivos e negativos observados
4. Destaque exemplos concretos do texto
5. Justifique didaticamente, como para outro professor

🔍 Em seguida, forneça **comentários por trecho problemático**, com:
- Qual é o problema
- Trecho exato
- Sugestão de reescrita

🧠 Finalize com uma **Análise Dialógica Geral**, considerando:
- Projeto de dizer do sujeito
- Coerência e progressão argumentativa
- Presença de vozes sociais
- Relação entre texto e contexto

Redação do aluno:
"""
{texto}
"""
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
