from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import UserAdd


class UserRepository(BaseRepository):
    model = UsersORM
    schema: BaseModel = UserAdd
    