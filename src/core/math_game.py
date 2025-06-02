import random

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
    agent_name = "👨‍🏫 Meester Papa"
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
