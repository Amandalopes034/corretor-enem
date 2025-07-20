import streamlit as st
import openai

st.set_page_config(page_title="Corretor ENEM Dialógico", layout="wide")
st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

openai_api_key = st.sidebar.text_input("🔐 Cole sua OpenAI API Key:", type="password")

texto = st.text_area("Cole sua redação aqui:", height=400)

if st.button("Corrigir Redação"):
    if not openai_api_key:
        st.warning("⚠️ Você precisa colar sua API Key para continuar.")
    elif not texto.strip():
        st.warning("⚠️ Cole sua redação antes de corrigir.")
    else:
        with st.spinner("Corrigindo, por favor aguarde..."):
            openai.api_key = openai_api_key

            prompt = f"""
Você é um avaliador experiente do ENEM e também um linguista com abordagem dialógica (inspirado em Bakhtin).

1. Identifique todos os trechos problemáticos no texto abaixo — problemas de argumentação, coerência, apagamento de vozes, silenciamento de sentidos, ou desvios enunciativos.
Para cada trecho, use o formato:

"Trecho problemático"
Comentário: explicação e sugestão de melhoria.

2. Depois, faça uma análise dialógica geral, considerando:
- Projeto de dizer
- Intenção discursiva
- Progressão do posicionamento
- Coerência enunciativa
- Presença ou ausência de vozes sociais

3. Por fim, atribua nota de 0 a 200 para cada competência do ENEM com justificativa curta:
- C1: Norma padrão
- C2: Compreensão da proposta
- C3: Argumentação
- C4: Coesão
- C5: Proposta de intervenção

Some a nota total (0 a 1000) no fim.

Redação:
{texto}
"""
            resposta = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Você é um avaliador crítico do ENEM com formação linguística dialógica."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )

            resultado = resposta['choices'][0]['message']['content']
            st.markdown("### Resultado da Correção:")
            st.write(resultado)
