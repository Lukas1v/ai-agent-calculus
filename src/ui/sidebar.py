import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("### 📚 Hoe werkt het?")
        st.markdown("""
        1. 🚀 Klik op 'Start Rekenen!'
        2. 🤔 Bekijk de rekensom
        3. ✏️ Typ je antwoord
        4. ✅ Klik op 'Antwoord'
        5. 💬 Lees de feedback
        6. 🔄 Bij een fout antwoord, probeer opnieuw!
        """)

        st.markdown("### 🎯 Score")
        st.markdown("""
        - **Goed**: Aantal vragen goed beantwoord
        - **Totaal**: Aantal vragen geprobeerd
        - **Score**: Percentage goed beantwoord
        
        *Elke vraag telt mee, ook als je hem fout hebt!*
        """)

        st.markdown("---")
        st.markdown("### 🛠️ Gemaakt met")
        st.markdown("- Streamlit")
        st.markdown("- LangChain") 
        st.markdown("- OpenAI GPT")
