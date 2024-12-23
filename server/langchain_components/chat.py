from typing import Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)


class ChatAssistant:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=api_key
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
