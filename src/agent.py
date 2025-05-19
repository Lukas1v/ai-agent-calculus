import random
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os


load_dotenv()  # Load from .env
agent_name="Meeste Papa"


# === LangChain Memory and Chat Model ===
memory = ConversationBufferMemory()
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)


def generate_problem():
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    operation = random.choice(['+', '-'])

    if operation == '-' and num2 > num1:
        num1, num2 = num2, num1

    question = f"Wat is {num1} {operation} {num2}?"
    correct_answer = eval(f"{num1} {operation} {num2}")
    return question, correct_answer


def get_feedback(correct, user_answer, correct_answer):
    system_prompt = (
        f"Je bent {agent_name}, een vriendelijke en vrolijke persoon die Vlaamse kinderen van zes jaar helpt met rekenen tot en met 20. "
        "Je spreekt altijd Nederlands, bent positief, gebruikt korte zinnen en eenvoudige woordjes die kinderen van 6 begrijpen. "
        "Je geeft complimentjes bij goede antwoorden, en uitleg of hints bij foutjes in max 3 korte zinnen. "
        "Je spreekt het kind direct aan."
    )

    if correct:
        user_prompt = (
            f"Het kind gaf het juiste antwoord: {user_answer}. "
            f"Geef een vriendelijk en enthousiast compliment als {agent_name}."
        )
    else:
        user_prompt = (
            f"Het kind gaf '{user_answer}', maar het juiste antwoord is '{correct_answer}'. "
            f"Leg als {agent_name} uit waarom het fout was, en geef een hint om het de volgende keer beter te doen."
        )

    # Use both system and user prompts
    return conversation.run(f"{system_prompt}\n\n{user_prompt}")


# === Main Program Loop ===
def run_math_agent():
    print(f"👩‍🏫 {agent_name}: Hallo daar! Zin om samen te rekenen?")
    print("Typ 'stop' om te stoppen.\n")

    while True:
        question, correct_answer = generate_problem()
        print(f"Vraag: {question}")
        user_input = input("Jouw antwoord: ")

        if user_input.lower() == "stop":
            print(f"👩‍🏫 {agent_name}: Goed gedaan vandaag! Tot snel weer!")
            break

        try:
            user_answer = int(user_input)
            correct = (user_answer == correct_answer)
            feedback = get_feedback(correct, user_answer, correct_answer)
            print(f"👩‍🏫 {agent_name}:", feedback)
        except ValueError:
            print(f"👩‍🏫 {agent_name}: Oeps! Typ alsjeblieft een getal.")

if __name__ == "__main__":
    run_math_agent()
