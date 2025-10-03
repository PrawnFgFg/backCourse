from fastapi import APIRouter, HTTPException, status, Response

from src.schemas.users import UserRequestADD, UserAdd
from src.services.auth import AuthService
from src.api.dependecies import UserIdDep
from src.api.dependecies import DBDep
from src.execptions import ObjectAlreadyExistsException

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data_add: UserRequestADD, db: DBDep):
    hashed_password = AuthService().hash_password(data_add.password)
    new_user_data = UserAdd(email=data_add.email, hashed_password=hashed_password)
    try:
        await db.users.add(schemas=new_user_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой email уже существует")
    await db.session.commit()
    return {"status": "Ok"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data_login: UserRequestADD,
    response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким email не зарегистрирован",
        )
    if not AuthService().verify_password(
        plain_password=data_login.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "Ok"}
