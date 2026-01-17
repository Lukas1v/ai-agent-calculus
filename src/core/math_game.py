import random
import streamlit as st

def generate_problem():
    # Get selected operations from session state
    selected_operations = st.session_state.get('selected_operations', ["Optellen", "Aftrekken"])

    if not selected_operations:
        selected_operations = ["Optellen", "Aftrekken"]

    # Choose a random operation from selected
    chosen_operation = random.choice(selected_operations)

    if chosen_operation == "Optellen":
        # Addition
        num1 = random.randint(1, 100)
        num2 = min(random.randint(1, 10), 100 - num1)
        question = f"Wat is {num1} + {num2}?"
        correct_answer = num1 + num2

    elif chosen_operation == "Aftrekken":
        # Subtraction
        num1 = random.randint(1, 100)
        num2 = min(random.randint(1, num1), 10)
        question = f"Wat is {num1} - {num2}?"
        correct_answer = num1 - num2

    else:
        # Multiplication table (e.g., "Tafel van 2")
        table_number = int(chosen_operation.split()[-1])

        # Randomly choose multiplication or division
        if random.choice([True, False]):
            # Multiplication
            num2 = random.randint(1, 10)
            question = f"Wat is {table_number} × {num2}?"
            correct_answer = table_number * num2
        else:
            # Division
            num2 = random.randint(1, 10)
            product = table_number * num2
            question = f"Wat is {product} ÷ {table_number}?"
            correct_answer = num2

    return question, correct_answer

def get_feedback(conversation, correct, user_answer, correct_answer):
    agent_name = "👨‍🏫 Meester Papa"
    system_prompt = (
        f"Je bent {agent_name}, een vriendelijke en vrolijke persoon die Vlaamse kinderen van zes jaar helpt met rekenen. "
        "Je spreekt altijd Nederlands, bent positief, gebruikt korte zinnen en eenvoudige woordjes die kinderen van 6 begrijpen. "
        "Je geeft complimentjes bij goede antwoorden, en uitleg bij foutjes in max 3 korte zinnen zonder het antwoord te verklappen. "
        "Je spreekt het kind direct aan."
    )

    if correct:
        user_prompt = (
            f"Het kind gaf het juiste antwoord: {user_answer}. "
            f"Geef een vriendelijk en enthousiast compliment als {agent_name} van 1 zin en max 6 woorden."
        )
    else:
        user_prompt = (
            f"Het kind gaf '{user_answer}', maar het juiste antwoord is '{correct_answer}'. "
            f"Leg uit als {agent_name} uit waarom het fout was aan de hand van tientallen en eenheden. Verklap het juiste antwoord niet maar laat het kind het zelf vinden."
        )

    response = conversation.invoke(
        {
            "system_message": system_prompt,
            "input": user_prompt
        },
        config={"configurable": {"session_id": "math_session"}}
    )

    return response.content
