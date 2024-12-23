from typing import Optional
from langchain.memory import ConversationBufferMemory


def get_memory(user_id: str) -> Optional[ConversationBufferMemory]:
    """Retorna a memória de conversação para um usuário"""
    try:
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
            input_key="input",
        )
    except Exception:
        return None
