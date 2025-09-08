from pydantic import BaseModel
from typing import Annotated
from fastapi import Query, Depends, Request, HTTPException, status

from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker

    
class PaginationParam(BaseModel):
    page: Annotated[int | None, Query(1, description="Номер страницы", gt=0)]
    per_page: Annotated[int | None, Query(None, description="Количество отелей на стр", gt=1, lt=30)]
    

PaginationDep = Annotated[PaginationParam, Depends()]


def get_token(request: Request):
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не придоставили токен доступа")
    return access_token 
    
def get_current_user(token: str = Depends(get_token)):
    user_data = AuthService().decode_token(token=token)
    return user_data["user_id"]   
    
UserIdDep = Annotated[int, Depends(get_current_user)]

def db_manager():
    return DBManager(session_factory=async_session_maker)

async def get_db():
    async with db_manager() as db:
        yield db



DBDep = Annotated[DBManager, Depends(get_db)]