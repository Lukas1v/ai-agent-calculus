import random

def generate_problem():
    max_number = 100
    operation = random.choice(['+', '-'])
    num1 = random.randint(1, max_number)

    if operation == '-':
        num2 = min(random.randint(1, num1),10)
    else:
        num2 = min(random.randint(1, 10), max_number - num1)

    question = f"Wat is {num1} {operation} {num2}?"
    correct_answer = eval(f"{num1} {operation} {num2}")
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
