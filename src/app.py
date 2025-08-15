# app.py
import streamlit as st
import time
from core.state import initialize_state, reset_game
from core.math_game import generate_problem, get_feedback
from core.langchain_setup import setup_langchain
from ui.sidebar import render_sidebar
from ui.scoreboard import render_scoreboard
from ui.feedback import render_feedback
import yaml
from pathlib import Path

# Load YAML config once at startup
CONFIG_PATH = Path(__file__).parent / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _config_data = yaml.safe_load(f)
AGENT_EMOJI = _config_data["agent"]["emoji"]
AGENT_NAME = _config_data["agent"]["name"]

agent_display_name = f"{AGENT_EMOJI} {AGENT_NAME}"

# Streamlit UI setup
st.set_page_config(
    page_title=f"Rekenen met {AGENT_NAME}",
    page_icon="🧮",
    layout="centered"
)

st.title(f"🧮 Rekenen met {AGENT_NAME}")
st.markdown("---")

# Initialize state and LangChain
initialize_state()
conversation = setup_langchain()

# Welcome / Start Game
if not st.session_state.game_started:
    st.markdown(f"### {agent_display_name}: Hallo daar! Zin om samen te rekenen?")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Rekenen!", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
else:
    render_scoreboard(agent_display_name)

    if st.session_state.current_question is None or st.session_state.question_answered:
        question, answer = generate_problem()
        st.session_state.current_question = question
        st.session_state.current_answer = answer
        st.session_state.question_answered = False

    st.markdown(f"### 🤔 {st.session_state.current_question}")
    col1, col2 = st.columns([3, 1])
    with col1:
        user_answer = st.number_input("Jouw antwoord:", min_value=0, max_value=40, step=1, key="answer_input")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        submit_answer = st.button("✅ Antwoord", type="primary")

    if submit_answer:
        correct = (user_answer == st.session_state.current_answer)
        st.session_state.total_count += 1

        if correct:
            st.session_state.correct_count += 1

            # 🎉 Show a unicorn gif at every multiple of 10 correct answers
            if st.session_state.correct_count % 10 == 0:
                st.image("src/assets/unicorn.gif", caption="🎉 Hoera! Goed bezig!", use_container_width=True)
                time.sleep(3)

        feedback = get_feedback(conversation, correct, user_answer, st.session_state.current_answer)
        st.session_state.feedback_history = [{
            "type": "success" if correct else "error",
            "message": feedback,
            "question": st.session_state.current_question,
            "answer": user_answer,
            "correct_answer": None if correct else st.session_state.current_answer
        }]

        st.session_state.question_answered = True
        st.rerun()

    render_feedback(agent_display_name)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔄 Nieuwe Vraag"):
            st.session_state.question_answered = True
            st.rerun()
    with col2:
        if st.button("🎮 Nieuw Spel"):
            reset_game()
            st.rerun()
    with col3:
        if st.button("🏁 Stop"):
            st.session_state.game_started = False
            st.markdown(f"### {agent_display_name}: Goed gedaan vandaag! Tot snel weer!")
            st.balloons()
            if st.button("🔄 Speel Opnieuw"):
                reset_game()
                st.rerun()

# Sidebar instructions
render_sidebar()
