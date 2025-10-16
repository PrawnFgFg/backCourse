from fastapi import APIRouter, Response

from src.schemas.users import UserRequestADD
from src.services.auth import AuthService
from src.api.dependecies import UserIdDep
from src.api.dependecies import DBDep
from src.execptions import UserAlreadyExist, UserAlreadyExistsHTTPException

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data_add: UserRequestADD, db: DBDep):
    try:
        await AuthService(db).register_user(data_add=data_add)
    except UserAlreadyExist:
        raise UserAlreadyExistsHTTPException
    return {"status": "Ok"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data_login: UserRequestADD,
    response: Response,
):
    access_token = await AuthService(db).login_user(data_login=data_login, response=response)
    return {"access_token": access_token}

@router.get('/me', summary="🤗 Мой профиль")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
# @router.get("/me")
# async def get_me(
#     user_id: UserIdDep,
#     db: DBDep,
# ):
#     user = await AuthService(db).get_me(user_id)
#     return user


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "Ok"}
