from pydantic import BaseModel
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room, RoomWithReals
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
        
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
                 )
            
        result = await self.session.execute(query)
        return [RoomWithReals.model_validate(model, from_attributes=True) for model in result.scalars().unique().all()]
    
    
    
    async def get_one_room_with_facilities(
        self,
        hotel_id: int,
        room_id: int,
    ):
        query = (
            select(RoomsORM)
            .filter_by(hotel_id=hotel_id, id=room_id)
            .options(selectinload(RoomsORM.facilities))
        )
        
        res = await self.session.execute(query)
        room_with_facilities = res.scalars().one()
        
        return RoomWithReals.model_validate(room_with_facilities, from_attributes=True)
        