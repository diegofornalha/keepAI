from typing import List, Optional, Dict, Any
from models.user import UserProfile
from config.database import SupabaseWrapper


class UserService:
    def __init__(self) -> None:
        self.db = SupabaseWrapper[UserProfile](UserProfile, "user_profiles")

    async def list_users(self) -> List[UserProfile]:
        return await self.db.select()

    async def get_user(self, user_id: str) -> Optional[UserProfile]:
        return await self.db.get_by_id(user_id)

    async def create_user(self, user_data: Dict[str, Any]) -> Optional[UserProfile]:
        return await self.db.insert(user_data)

    async def update_user(
        self, user_id: str, user_data: Dict[str, Any]
    ) -> Optional[UserProfile]:
        return await self.db.update(user_id, user_data)

    async def delete_user(self, user_id: str) -> bool:
        return await self.db.delete(user_id)
