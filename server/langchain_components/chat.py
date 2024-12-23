from typing import Dict, Any
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)


class ChatAssistant:
    def __init__(self, api_key: str) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            api_key=SecretStr(api_key),
            temperature=0.7,
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "Você é um assistente útil e amigável. "
                    "Ajude o usuário com suas notas, tarefas e eventos."
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        self.chain = ConversationChain(
            llm=self.llm, memory=self.memory, prompt=self.prompt, verbose=True
        )

    def process_message(self, message: str) -> Dict[str, Any]:
        try:
            response = self.chain.predict(input=message)
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}


def get_chat(api_key: str) -> ChatGoogleGenerativeAI:
    """Retorna uma instância de ChatGoogleGenerativeAI"""
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        api_key=SecretStr(api_key),
        temperature=0.7,
    )
