import streamlit as st
import openai
import os

# 🎨 Oculta a barra lateral
hide_sidebar = """
<style>
    [data-testid="stSidebar"] {display: none;}
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# 🚀 Configuração da página
st.set_page_config(page_title="Corretor ENEM Dialógico", layout="wide")
st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

# 🔐 Chave de API via variável secreta
openai.api_key = os.environ["OPENAI_API_KEY"]

# 📝 Campo de entrada da redação
texto = st.text_area("Cole sua redação aqui:", height=400)

# ▶️ Botão para acionar correção
if st.button("Corrigir Redação"):
    if not texto.strip():
        st.warning("⚠️ Por favor, cole uma redação antes de corrigir.")
    else:
        with st.spinner("⏳ Corrigindo... isso pode levar alguns segundos"):
            prompt = f"""
Você é um avaliador experiente do ENEM e também um linguista com abordagem dialógica (inspirado em Bakhtin).

Sua tarefa é:
1. Ler a redação abaixo e identificar **todos os trechos problemáticos**, como:
- Argumentação fraca ou contraditória
- Problemas de coesão ou progressão
- Apagamento de vozes sociais
- Silenciamento de sentidos
- Problemas enunciativos

Para cada trecho, use o formato:
"Trecho problemático"
Comentário: explicação do problema e sugestão de melhoria.

2. Em seguida, faça uma **análise linguística dialógica geral**, considerando:
- O projeto de dizer do autor
- A progressão argumentativa
- Presença ou ausência de vozes sociais
- Coerência enunciativa

3. Depois, atribua uma nota de 0 a 200 para cada competência do ENEM com justificativa curta:
- C1: Norma padrão
- C2: Compreensão da proposta
- C3: Organização dos argumentos
- C4: Coesão textual
- C5: Proposta de intervenção

4. Por fim, forneça a **nota final de 0 a 1000**.

Redação:
{texto}
"""

            resposta = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Você é um corretor do ENEM com formação linguística dialógica."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )

            resultado = resposta['choices'][0]['message']['content']

            st.markdown("## 📄 Resultado da Correção:")
            st.markdown("---")
            st.markdown(resultado)
