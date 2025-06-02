import streamlit as st

def render_scoreboard(agent_name):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Goed", st.session_state.correct_count)
    with col2:
        st.metric("📊 Totaal", st.session_state.total_count)
    with col3:
        if st.session_state.total_count > 0:
            percentage = round((st.session_state.correct_count / st.session_state.total_count) * 100)
            st.metric("🎯 Score", f"{percentage}%")
        else:
            st.metric("🎯 Score", "0%")
    st.markdown("---")
