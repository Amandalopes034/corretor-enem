import streamlit as st
import openai
import os

# 🔐 Chave da OpenAI via secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Configuração da interface
st.set_page_config(page_title="Corretor ENEM - GPT-4", layout="wide")
st.title("📝 Corretor de Redações ENEM com Análise Dialógica (GPT-4)")

st.markdown("Cole abaixo sua redação. A análise incluirá comentários por trecho, leitura dialógica e notas com base nas 5 competências do ENEM.")

# Entrada da redação
redacao = st.text_area("Cole sua redação aqui:", height=350)

# Botão de correção
if st.button("Corrigir Redação"):
    if not redacao.strip():
        st.warning("⚠️ Por favor, cole sua redação antes de enviar.")
        st.stop()

    with st.spinner("Analisando com GPT-4..."):

        prompt = f"""
Você é um corretor oficial do ENEM com formação em análise linguística dialógica.

Leia a redação abaixo e produza:

1. Comentários por trechos com problemas. Para cada trecho:
   - Destaque o texto problemático entre aspas
   - Faça um comentário explicativo, apontando o problema e sugerindo melhorias

2. Uma análise dialógica geral, considerando:
   - Projeto de dizer do sujeito
   - Coerência e progressão argumentativa
   - Presença (ou ausência) de vozes sociais
   - Relação entre texto e contexto

3. Atribua nota (0 a 200) para cada uma das 5 competências do ENEM, com justificativas curtas:
   - C1: Norma padrão
   - C2: Compreensão da proposta
   - C3: Organização dos argumentos
   - C4: Coesão textual
   - C5: Proposta de intervenção

4. Informe a nota final (0 a 1000), soma das cinco competências.

Redação:
\"\"\"{redacao}\"\"\"
"""

        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Você é um avaliador ENEM com abordagem linguística dialógica."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1800  # pode ajustar pra caber mais saída se quiser
            )

            resultado = resposta["choices"][0]["message"]["content"]

            # Resultado
            st.subheader("✅ Resultado da Correção")
            st.markdown("---")
            st.markdown(resultado)

        except Exception as e:
            st.error(f"❌ Erro ao acessar a API: {e}")
