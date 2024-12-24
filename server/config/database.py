from typing import TypeVar, Generic, List, Optional, Dict, Any, cast
from supabase import create_client
from pydantic import BaseModel
from postgrest.request_builder import SelectRequestBuilder

from config.settings import settings

T = TypeVar("T", bound=BaseModel)


class SupabaseWrapper(Generic[T]):
    def __init__(self, model_class: type[T], table_name: str) -> None:
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.model_class = model_class
        self.table_name = table_name

    def _validate_model(self, data: Dict[str, Any]) -> T:
        return self.model_class(**data)

    async def select(self, query: Optional[Dict[str, Any]] = None) -> List[T]:
        response = await cast(
            SelectRequestBuilder, self.client.table(self.table_name).select("*")
        ).execute()
        data = response.data
        return [self._validate_model(item) for item in data]

    async def get_by_id(self, id: str) -> Optional[T]:
        response = await cast(
            SelectRequestBuilder,
            self.client.table(self.table_name).select("*").eq("id", id).single(),
        ).execute()
        if not response.data:
            return None
        return self._validate_model(response.data)

    async def insert(self, data: Dict[str, Any]) -> T:
        response = await cast(
            SelectRequestBuilder, self.client.table(self.table_name).insert(data)
        ).execute()
        return self._validate_model(response.data[0])

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[T]:
        response = await cast(
            SelectRequestBuilder,
            self.client.table(self.table_name).update(data).eq("id", id),
        ).execute()
        if not response.data:
            return None
        return self._validate_model(response.data[0])

    async def delete(self, id: str) -> bool:
        response = await cast(
            SelectRequestBuilder,
            self.client.table(self.table_name).delete().eq("id", id),
        ).execute()
        return bool(response.data)


supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
