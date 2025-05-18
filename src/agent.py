import random
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os


load_dotenv()  # Load from .env



# === LangChain Memory and Chat Model ===
memory = ConversationBufferMemory()
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# === Generate Math Problem ===
def generate_problem():
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    operation = random.choice(['+', '-'])

    if operation == '-' and num2 > num1:
        num1, num2 = num2, num1

    question = f"Wat is {num1} {operation} {num2}?"
    correct_answer = eval(f"{num1} {operation} {num2}")
    return question, correct_answer

# === Juf Lotte speaks ===
def get_feedback(correct, user_answer, correct_answer):
    system_prompt = (
        "Je bent Juf Lotte, een vriendelijke en vrolijke juf die Nederlandse kinderen van zes jaar helpt met rekenen tot en met 20. "
        "Je spreekt altijd Nederlands, bent positief, gebruikt korte zinnen en eenvoudige woordjes. "
        "Je geeft complimentjes bij goede antwoorden, en uitleg of hints bij foutjes. "
        "Je spreekt het kind direct aan."
    )

    if correct:
        user_prompt = (
            f"Het kind gaf het juiste antwoord: {user_answer}. "
            f"Geef een vriendelijk en enthousiast compliment als Juf Lotte."
        )
    else:
        user_prompt = (
            f"Het kind gaf '{user_answer}', maar het juiste antwoord is '{correct_answer}'. "
            f"Leg als Juf Lotte uit waarom het fout was, en geef een hint om het de volgende keer beter te doen."
        )

    # Use both system and user prompts
    return conversation.run(f"{system_prompt}\n\n{user_prompt}")

# === Main Program Loop ===
def run_math_agent():
    print("👩‍🏫 Juf Lotte: Hallo daar! Zin om samen te rekenen?")
    print("Typ 'stop' om te stoppen.\n")

    while True:
        question, correct_answer = generate_problem()
        print(f"Vraag: {question}")
        user_input = input("Jouw antwoord: ")

        if user_input.lower() == "stop":
            print("👩‍🏫 Juf Lotte: Goed gedaan vandaag! Tot snel weer!")
            break

        try:
            user_answer = int(user_input)
            correct = (user_answer == correct_answer)
            feedback = get_feedback(correct, user_answer, correct_answer)
            print("👩‍🏫 Juf Lotte:", feedback)
        except ValueError:
            print("👩‍🏫 Juf Lotte: Oeps! Typ alsjeblieft een getal.")

if __name__ == "__main__":
    run_math_agent()
