import streamlit as st

def initialize_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.correct_count = 0
        st.session_state.total_count = 0
        st.session_state.current_question = None
        st.session_state.current_answer = None
        st.session_state.question_answered = True
        st.session_state.feedback_history = []
        st.session_state.game_started = False

def reset_game():
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.question_answered = True
    st.session_state.feedback_history = []
    st.session_state.game_started = False
