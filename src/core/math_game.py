import random
import streamlit as st
import yaml
from pathlib import Path

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _config = yaml.safe_load(f)
AGENT_NAME = _config["agent"]["name"]

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
        num2 = min(random.randint(1, 30), 100 - num1)
        question = f"Wat is {num1} + {num2}?"
        correct_answer = num1 + num2

    elif chosen_operation == "Aftrekken":
        # Subtraction
        num1 = random.randint(1, 100)
        num2 = min(random.randint(1, num1), 30)
        question = f"Wat is {num1} - {num2}?"
        correct_answer = num1 - num2

    elif chosen_operation == "Helft en kwart":
        # Half or quarter calculation
        # Randomly choose between half or quarter
        if random.choice([True, False]):
            # Half - number must be divisible by 2
            num = random.randint(1, 50) * 2  # Ensures divisible by 2
            question = f"Wat is de helft van {num}?"
            correct_answer = num // 2
        else:
            # Quarter - number must be divisible by 4
            num = random.randint(1, 25) * 4  # Ensures divisible by 4
            question = f"Wat is een kwart van {num}?"
            correct_answer = num // 4

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
    system_prompt = (
        f"Je bent een vriendelijke en positieve rekenleraar die kinderen van zes jaar helpt met wiskunde. "
        "Je spreekt altijd Nederlands, bent positief, gebruikt korte zinnen en eenvoudige woordjes die kinderen van 6 begrijpen. "
        "Je geeft complimentjes bij goede antwoorden, en uitleg bij foutjes in max 3 korte zinnen zonder het antwoord te verklappen. "
        "Je spreekt het kind direct aan."
    )

    if correct:
        user_prompt = (
            f"Het kind gaf het juiste antwoord: {user_answer}. "
            f"Geef een vriendelijk en enthousiast compliment van 1 zin en max 6 woorden."
        )
    else:
        user_prompt = (
            f"Het kind gaf '{user_answer}', maar het juiste antwoord is '{correct_answer}'. "
            f"Leg uit waarom het fout was aan de hand van tientallen en eenheden. Verklap het juiste antwoord niet maar laat het kind het zelf vinden."
        )

    response = conversation.invoke(
        {
            "system_message": system_prompt,
            "input": user_prompt
        },
        config={"configurable": {"session_id": "math_session"}}
    )

    return response.content
