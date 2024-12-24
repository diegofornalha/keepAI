from typing import Optional, List
from uuid import UUID

from models.user import UserProfile
from config.database import supabase_client


class UserService:
    """Serviço para gerenciamento de usuários."""

    @staticmethod
    async def get_profile(user_id: UUID) -> Optional[UserProfile]:
        """Busca o perfil de um usuário."""
        try:
            response = (
                await supabase_client.table("profiles")
                .select("*")
                .eq("id", str(user_id))
                .single()
            )
            if response.data:
                return UserProfile.model_validate(response.data)
            return None
        except Exception as e:
            print(f"Erro ao buscar perfil: {e}")
            return None

    @staticmethod
    async def update_profile(
        user_id: UUID, profile_data: dict
    ) -> Optional[UserProfile]:
        """Atualiza o perfil de um usuário."""
        try:
            response = (
                await supabase_client.table("profiles")
                .update(profile_data)
                .eq("id", str(user_id))
                .execute()
            )
            if response.data:
                return UserProfile.model_validate(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")
            return None

    @staticmethod
    async def list_profiles() -> List[UserProfile]:
        """Lista todos os perfis."""
        try:
            response = await supabase_client.table("profiles").select("*").execute()
            return [UserProfile.model_validate(profile) for profile in response.data]
        except Exception as e:
            print(f"Erro ao listar perfis: {e}")
            return []

    @staticmethod
    async def delete_profile(user_id: UUID) -> bool:
        """Deleta um perfil."""
        try:
            response = (
                await supabase_client.table("profiles")
                .delete()
                .eq("id", str(user_id))
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao deletar perfil: {e}")
            return False
