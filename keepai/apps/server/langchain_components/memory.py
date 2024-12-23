import os
from typing import Any, Dict, List

from langchain.memory import ConversationBufferMemory
from server.config.settings import settings


class SupabaseMemory(ConversationBufferMemory):
    def __init__(self):
        super().__init__()
        self.supabase = settings.get_supabase_client()
        self.table_name = "conversations"

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Salva o contexto da conversa no Supabase."""
        try:
            self.supabase.table(self.table_name).insert(
                {"inputs": inputs, "outputs": outputs, "session_id": self.session_id}
            ).execute()
        except Exception as e:
            print(f"Erro ao salvar contexto: {e}")

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Carrega variáveis da memória do Supabase."""
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("inputs, outputs")
                .eq("session_id", self.session_id)
                .order("created_at", desc=True)
                .limit(10)
                .execute()
            )

            history = []
            for item in result.data:
                history.extend(
                    [
                        {"role": "user", "content": str(item["inputs"])},
                        {"role": "assistant", "content": str(item["outputs"])},
                    ]
                )

            return {"history": history}
        except Exception as e:
            print(f"Erro ao carregar memória: {e}")
            return {"history": []}
