from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
import sys

# Force reload of environment variables
load_dotenv(override=True)

def setup_langchain():
    # Check if Azure OpenAI credentials are provided
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if azure_endpoint and azure_api_key:
        # Use Azure OpenAI
        print(f"🔵 Using Azure OpenAI endpoint: {azure_endpoint}")
        llm = AzureChatOpenAI(
            temperature=0.6,
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
    else:
        # Fallback to regular OpenAI
        print("⚠️ Azure credentials not found, falling back to OpenAI")
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
