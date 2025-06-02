import streamlit as st

def render_feedback(agent_name):
    if st.session_state.feedback_history:
        st.markdown("---")
        st.markdown("### 💬 Feedback")

        recent_feedback = st.session_state.feedback_history[-3:]
        for feedback in reversed(recent_feedback):
            if feedback["type"] == "success":
                st.success(f"{agent_name}: {feedback['message']}")
            else:
                st.error(f"{agent_name}: {feedback['message']}")
                if "correct_answer" in feedback:
                    st.info(f"Het juiste antwoord was: {feedback['correct_answer']}")
