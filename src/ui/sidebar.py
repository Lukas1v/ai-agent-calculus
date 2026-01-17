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
        st.markdown("### 🎲 Kies je oefeningen")

        # Define all operation options
        operation_options = [
            "Optellen",
            "Aftrekken",
            "Tafel van 2",
            "Tafel van 3",
            "Tafel van 4",
            "Tafel van 5",
            "Tafel van 6",
            "Tafel van 7",
            "Tafel van 8",
            "Tafel van 9",
            "Tafel van 10"
        ]

        # Store selected operations in session state
        if 'selected_operations' not in st.session_state:
            st.session_state.selected_operations = ["Optellen", "Aftrekken"]

        selected = st.multiselect(
            "Selecteer oefeningen:",
            options=operation_options,
            default=st.session_state.selected_operations,
            key="operation_selector"
        )

        # Update session state with new selection
        if selected:
            st.session_state.selected_operations = selected
        else:
            st.info("⚠️ Kies minstens één oefening!")
