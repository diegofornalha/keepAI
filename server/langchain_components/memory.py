from typing import Dict, Any
from langchain.memory import ConversationBufferMemory


class ChatMemory:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    def add_message(self, message: str, response: str) -> Dict[str, Any]:
        try:
            self.memory.save_context({"input": message}, {"output": response})
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_history(self) -> Dict[str, Any]:
        try:
            history = self.memory.load_memory_variables({})
            return {"success": True, "history": history}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def clear(self) -> Dict[str, Any]:
        try:
            self.memory.clear()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
