from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UserRepository
from src.schemas.users import UserRequestADD, UserAdd


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post("/register")
async def register_user(data_add: UserRequestADD):
    hashed_password = pwd_context.hash(data_add.password)
    new_user_data = UserAdd(email=data_add.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            user = await UserRepository(session).add(schemas=new_user_data)
            check_user = await UserRepository(session).get_one_or_none(email=user.email)
            
        except SQLAlchemyError('Пользователь с таким email уже существует') as e:
            await session.rollback()
            raise e
        
        await session.commit()
    return {"status": "Ok"}