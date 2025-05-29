import streamlit as st
import random
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configuration
agent_name = "Meester Papa"

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.question_answered = True  # Start with generating new question
    st.session_state.feedback_history = []
    st.session_state.game_started = False

# Set up LangChain components
@st.cache_resource
def setup_langchain():
    llm = ChatOpenAI(temperature=0.6, model="gpt-4o-mini")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_message}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    store = {}
    
    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    conversation = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    
    return conversation

def generate_problem():
    max_number = 20
    operation = random.choice(['+', '-'])
    num1 = random.randint(0, max_number)
    
    if operation == '-':
        num2 = random.randint(0, num1)
    else:
        num2 = min(random.randint(0, 10), max_number - num1)
    
    question = f"Wat is {num1} {operation} {num2}?"
    correct_answer = eval(f"{num1} {operation} {num2}")
    return question, correct_answer

def get_feedback(conversation, correct, user_answer, correct_answer):
    system_prompt = (
        f"Je bent {agent_name}, een vriendelijke en vrolijke persoon die Vlaamse kinderen van zes jaar helpt met rekenen tot en met 20. "
        "Je spreekt altijd Nederlands, bent positief, gebruikt korte zinnen en eenvoudige woordjes die kinderen van 6 begrijpen. "
        "Je geeft complimentjes bij goede antwoorden, en uitleg of hints bij foutjes in max 3 korte zinnen. "
        "Je spreekt het kind direct aan."
    )
    
    if correct:
        user_prompt = (
            f"Het kind gaf het juiste antwoord: {user_answer}. "
            f"Geef een vriendelijk en enthousiast compliment als {agent_name} van 1 zin en max 4 woorden."
        )
    else:
        user_prompt = (
            f"Het kind gaf '{user_answer}', maar het juiste antwoord is '{correct_answer}'. "
            f"Leg als {agent_name} uit waarom het fout was, en geef een hint om het de volgende keer beter te doen."
        )
    
    response = conversation.invoke(
        {
            "system_message": system_prompt,
            "input": user_prompt
        },
        config={"configurable": {"session_id": "math_session"}}
    )
    
    return response.content

def reset_game():
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.question_answered = True  # Start with generating new question
    st.session_state.feedback_history = []
    st.session_state.game_started = False

# Streamlit UI
st.set_page_config(
    page_title="🧮 Reken met Meester Papa",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Reken met Meester Papa")
st.markdown("---")

# Initialize LangChain
conversation = setup_langchain()

# Welcome message and start button
if not st.session_state.game_started:
    st.markdown(f"### 👨‍🏫 {agent_name}: Hallo daar! Zin om samen te rekenen?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Rekenen!", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()

else:
    # Score display
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
    
    # Generate new question if needed
    if st.session_state.current_question is None or st.session_state.question_answered:
        question, answer = generate_problem()
        st.session_state.current_question = question
        st.session_state.current_answer = answer
        st.session_state.question_answered = False
    
    # Display current question
    st.markdown(f"### 🤔 {st.session_state.current_question}")
    
    # Answer input
    col1, col2 = st.columns([3, 1])
    with col1:
        user_answer = st.number_input(
            "Jouw antwoord:",
            min_value=0,
            max_value=40,
            step=1,
            key="answer_input"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        submit_answer = st.button("✅ Antwoord", type="primary")
    
    # Process answer
    if submit_answer:
        correct = (user_answer == st.session_state.current_answer)
        st.session_state.total_count += 1
        
        if correct:
            st.session_state.correct_count += 1
            
            # Get feedback from AI
            feedback = get_feedback(conversation, True, user_answer, st.session_state.current_answer)
            st.session_state.feedback_history.append({
                "type": "success",
                "message": feedback,
                "question": st.session_state.current_question,
                "answer": user_answer
            })
            
        else:
            # Wrong answer - get feedback and move to next question
            feedback = get_feedback(conversation, False, user_answer, st.session_state.current_answer)
            st.session_state.feedback_history.append({
                "type": "error",
                "message": feedback,
                "question": st.session_state.current_question,
                "answer": user_answer,
                "correct_answer": st.session_state.current_answer
            })
        
        # Always move to next question after any answer
        st.session_state.question_answered = True
        st.rerun()
    
    # Display feedback history
    if st.session_state.feedback_history:
        st.markdown("---")
        st.markdown("### 💬 Feedback")
        
        # Show only the last few feedback messages to keep it clean
        recent_feedback = st.session_state.feedback_history[-3:]
        
        for feedback in reversed(recent_feedback):
            if feedback["type"] == "success":
                st.success(f"👨‍🏫 {agent_name}: {feedback['message']}")
            else:
                st.error(f"👨‍🏫 {agent_name}: {feedback['message']}")
                if "correct_answer" in feedback:
                    st.info(f"Het juiste antwoord was: {feedback['correct_answer']}")
    
    # Control buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Nieuwe Vraag", help="Sla deze vraag over"):
            # Skip question without counting it in total (matches original script logic)
            st.session_state.question_answered = True
            st.rerun()
    
    with col2:
        if st.button("🎮 Nieuw Spel", help="Begin opnieuw"):
            reset_game()
            st.rerun()
    
    with col3:
        if st.button("🏁 Stop", help="Stop het spel"):
            st.session_state.game_started = False
            st.markdown(f"### 👨‍🏫 {agent_name}: Goed gedaan vandaag! Tot snel weer!")
            st.balloons()
            if st.button("🔄 Speel Opnieuw"):
                reset_game()
                st.rerun()

# Sidebar with instructions
with st.sidebar:
    st.markdown("### 📚 Hoe werkt het?")
    st.markdown("""
    1. 🚀 Klik op 'Start Rekenen!'
    2. 🤔 Bekijk de rekensom
    3. ✏️ Typ je antwoord
    4. ✅ Klik op 'Antwoord'
    5. 💬 Lees de feedback van Meester Papa
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