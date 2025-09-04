from pydantic import BaseModel, EmailStr
from sqlalchemy import select, Result

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword


class UserRepository(BaseRepository):
    model = UsersORM
    schema: BaseModel = User
    
    
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        res: Result = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
    