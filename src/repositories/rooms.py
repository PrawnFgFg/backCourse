from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room



class RoomRepository(BaseRepository):
    model = RoomsORM
    schema: BaseModel = Room