tiva linguística/discursiva.
  - Uma pergunta provocadora para ajudar o aluno a refletir.

No fim da análise, apresente uma Síntese Dialógica Geral, com base na ALD:
- Qual é o projeto de dizer do sujeito?
- Há coerência e progressão argumentativa?
- Quais vozes sociais aparecem no texto? Elas dialogam entre si?
- Que efeitos de sentido o texto produz em relação ao tema proposto?
- O que a linguagem revela sobre o posicionamento do aluno diante do tema?

Use linguagem acessível, mas crítica. Fale com o aluno como um mentor reflexivo.

Redação do aluno:
"""

if st.button("🧠 Analisar Redação com Devolutiva Dialógica") and texto:
    with st.spinner("Gerando análise crítica e dialógica da redação..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": construir_prompt(texto) + texto}],
                temperature=0.3
            )
            devolutiva = response.choices[0].message.content

            st.markdown("## ✅ Devolutiva Dialógica da Redação")
            st.write(devolutiva)

            if st.button("📄 Gerar PDF da Devolutiva"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for linha in devolutiva.split('\n'):
                    pdf.multi_cell(0, 10, linha)
                pdf.output("devolutiva_dialógica.pdf")
                with open("devolutiva_dialógica.pdf", "rb") as f:
                    st.download_button("📥 Baixar PDF da Devolutiva", f, file_name="devolutiva_redacao_enem.pdf")

        except Exception as e:
            st.error(f"Erro durante a análise: {str(e)}")
