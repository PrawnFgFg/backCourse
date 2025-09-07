from pydantic import BaseModel
from datetime import date
from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room
from src.database import engine
from src.repositories.utils import rooms_ids_for_booking


class RoomRepository(BaseRepository):
    model = RoomsORM
    schema: BaseModel = Room
    
    
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
        ):
        
        # print(availavle_rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))