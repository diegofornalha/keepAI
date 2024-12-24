from typing import List
from fastapi import APIRouter, HTTPException
from models.user import UserProfile, UserProfileCreate, UserProfileUpdate
from services.user_service import UserService

router = APIRouter()
service = UserService()


@router.get("/profiles", response_model=List[UserProfile])
async def list_profiles() -> List[UserProfile]:
    return await service.list_users()


@router.get("/profiles/{user_id}", response_model=UserProfile)
async def get_profile(user_id: str) -> UserProfile:
    profile = await service.get_user(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/profiles", response_model=UserProfile)
async def create_profile(profile: UserProfileCreate) -> UserProfile:
    result = await service.create_user(profile.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Could not create profile")
    return result


@router.put("/profiles/{user_id}", response_model=UserProfile)
async def update_profile(user_id: str, profile: UserProfileUpdate) -> UserProfile:
    result = await service.update_user(user_id, profile.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Profile not found")
    return result


@router.delete("/profiles/{user_id}")
async def delete_profile(user_id: str) -> bool:
    if not await service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    return True
