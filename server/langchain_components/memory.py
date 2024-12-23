from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from typing import Optional
import os

class CustomBufferMemory(ConversationBufferMemory):
    def __init__(self, session_id: str):
        connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        
        message_history = SQLChatMessageHistory(
            session_id=session_id,
            connection_string=connection_string
        )
        
        super().__init__(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=message_history
        )
        
    async def clear(self):
        """Limpa o histórico de mensagens"""
        await self.chat_memory.clear() 