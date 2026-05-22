from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.models.user import User, UserRole
from fastapi import HTTPException, status


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def signup(self, email: str, password: str, full_name: str, phone: Optional[str] = None,
                     preferred_language: str = "en", location: Optional[str] = None,
                     farm_size: Optional[float] = None, soil_type: Optional[str] = None) -> User:
        if await self.repo.email_exists(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        if phone:
            existing = await self.repo.get_by_phone(phone)
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number already registered")
        user = await self.repo.create(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            phone=phone,
            preferred_language=preferred_language,
            location=location,
            farm_size=farm_size,
            soil_type=soil_type,
            role=UserRole.FARMER,
            is_verified=False,
        )
        return user

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
        refresh_token = create_refresh_token(data={"sub": str(user.id), "role": user.role.value})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800,
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user_id = payload.get("sub")
        user = await self.repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id), "role": user.role.value})
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": 1800,
        }

    async def change_password(self, user_id: int, current_password: str, new_password: str) -> None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        await self.repo.update_by_id(user_id, password_hash=hash_password(new_password))

    async def get_profile(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_profile(self, user_id: int, **kwargs) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if not clean_kwargs:
            return user
        updated = await self.repo.update_by_id(user_id, **clean_kwargs)
        return updated
