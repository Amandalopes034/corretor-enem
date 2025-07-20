import streamlit as st
import openai

# 🎨 Oculta a barra lateral (não será usada)
hide_sidebar = """
<style>
    [data-testid="stSidebar"] {display: none;}
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# 🚀 Configurações da página
st.set_page_config(page_title="Corretor ENEM Dialógico", layout="wide")
st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

# 🔐 CHAVE API
openai_api_key = "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"  # ⬅️ Substitua pelo seu sk-...
openai.api_key = openai_api_key

# 📝 Campo para colar a redação
texto = st.text_area("Cole sua redação aqui:", height=400)

# ▶️ Botão de correção
if st.button("Corrigir Redação"):
    if not texto.strip():
        st.warning("⚠️ Por favor, cole uma redação antes de corrigir.")
    else:
        with st.spinner("⏳ Corrigindo..."):
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
Comentário: explicação e sugestão de melhoria.

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
