from fastapi import APIRouter, HTTPException, status, Response, Depends

from src.database import async_session_maker
from src.repositories.users import UserRepository
from src.schemas.users import UserRequestADD, UserAdd
from src.services.auth import AuthService
from src.api.dependecies import UserIdDep, get_token



router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])



@router.post("/register")
async def register_user(data_add: UserRequestADD):
    hashed_password = AuthService().hash_password(data_add.password)
    new_user_data = UserAdd(email=data_add.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UserRepository(session).add(schemas=new_user_data)
        await session.commit()
    return {"status": "Ok"}


@router.post('/login')
async def login_user(
    data_login: UserRequestADD,
    response: Response,
    ):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_user_with_hashed_password(email=data_login.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(plain_password=data_login.password, hashed_password=user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    
    

@router.get("/me")
async def get_me(
    user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await  UserRepository(session).get_one_or_none(id=user_id)
        
    return user


@router.delete("/logout")
async def logout_user(
    response: Response,
    access_token: str = Depends(get_token),
):
    response.delete_cookie("access_token")
    return {"status": "Ok"}
    
    
    
    
    