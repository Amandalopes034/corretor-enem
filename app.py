import streamlit as st
import openai
import os

# Chave via secrets
openai.api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(page_title="Corretor de Redações - ENEM com Análise Dialógica")

st.title("📝 Corretor de Redações - ENEM com Análise Dialógica")

# Entrada de texto
texto = st.text_area("Cole sua redação abaixo:", height=300)

# Botão
if st.button("Corrigir Redação"):

    with st.spinner("Analisando sua redação..."):

        prompt = f"""
Você é um corretor experiente do ENEM com formação em linguística e análise dialógica.

Sua tarefa é ler a redação abaixo e gerar uma correção detalhada em **três blocos principais**:

---

**1. Comentários por trechos problemáticos**  
Para cada trecho com problemas, siga este formato:
- Trecho entre aspas
- Problema identificado com clareza
- Explicação do impacto do problema
- Sugestão clara de reescrita ou melhoria

---

**2. Análise dialógica geral**, cobrindo os seguintes aspectos:
- Projeto de dizer do sujeito
- Coerência e progressão argumentativa
- Presença (ou ausência) de vozes sociais
- Relação entre texto e contexto

---

**3. Avaliação das 5 competências do ENEM**  
Siga o formato abaixo, sendo **detalhista nas justificativas**:

**C1: Norma padrão**  
Nota (0-200): X  
Justificativa: [explique detalhadamente o uso da ortografia, concordância, pontuação, regência, crase, etc. Dê exemplos concretos.]

**C2: Compreensão da proposta**  
Nota (0-200): X  
Justificativa: [explique como o texto atende à proposta, se tangenciou, como interpreta o tema, etc.]

**C3: Organização dos argumentos**  
Nota (0-200): X  
Justificativa: [explique a estrutura textual, progressão das ideias, repetições, falhas argumentativas etc.]

**C4: Coesão textual**  
Nota (0-200): X  
Justificativa: [explique o uso de conectivos, retomadas, articulações entre frases e parágrafos.]

**C5: Proposta de intervenção**  
Nota (0-200): X  
Justificativa: [explique se há proposta clara, agentes, ações, meios, finalidade e detalhamento suficiente.]

---

Ao final, diga:  
**Nota final: X/1000** (soma das competências)

Redação a ser avaliada:
\"\"\"{texto}\"\"\"
"""

        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.4,
            )

            correcao = resposta.choices[0].message["content"]
            st.markdown(correcao)

        except Exception as e:
            st.error(f"Erro ao acessar a API da OpenAI: {e}")
