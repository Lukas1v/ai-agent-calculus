import random
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env
agent_name = "Meester Papa"

# === LangChain Memory and Chat Model ===
memory = ConversationBufferMemory()
llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo")
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

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
            f"Geef een vriendelijk en enthousiast compliment als {agent_name} van 1 zin en max 4 woorden."
        )
    else:
        user_prompt = (
            f"Het kind gaf '{user_answer}', maar het juiste antwoord is '{correct_answer}'. "
            f"Leg als {agent_name} uit waarom het fout was, en geef een hint om het de volgende keer beter te doen."
        )

    return conversation.run(f"{system_prompt}\n\n{user_prompt}")


# === Main Program Loop ===
def run_math_agent():
    correct_count = 0
    total_count = 0

    print(f"👩‍🏫 {agent_name}: Hallo daar! Zin om samen te rekenen?")
    print("Typ 'stop' om te stoppen.\n")

    while True:
        question, correct_answer = generate_problem()
        print(f"Vraag: {question}")
        user_input = input("Jouw antwoord: ")

        if user_input.lower() == "stop":
            print(f"\n👩‍🏫 {agent_name}: Goed gedaan vandaag! Tot snel weer!")
            print(f"🎯 Je score: {correct_count} van de {total_count} goed beantwoord!")
            break

        try:
            user_answer = int(user_input)
            correct = (user_answer == correct_answer)
            total_count += 1
            if correct:
                correct_count += 1
            feedback = get_feedback(correct, user_answer, correct_answer)
            print(f"👩‍🏫 {agent_name}:", feedback)
        except ValueError:
            print(f"👩‍🏫 {agent_name}: Oeps! Typ alsjeblieft een getal.")

if __name__ == "__main__":
    run_math_agent()
