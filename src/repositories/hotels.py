from datetime import date

from src.repositories.base import BaseRepository
from src.models.hotels import HotelORM
from src.models.rooms import RoomsORM
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_ids_for_booking
from sqlalchemy import select
from pydantic import BaseModel


class HotelRepository(BaseRepository):
    model = HotelORM
    schema: BaseModel = Hotel
    

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location: str | None = None,
        title: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to) 
        
        hotels_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
            )
        
        query = select(HotelORM).filter(HotelORM.id.in_(hotels_ids))
        
        if location: 
            query = query.filter(HotelORM.location.ilike(f'%{location.strip()}%'))
        if title:
            query = query.filter(HotelORM.title.ilike(f'%{title.strip()}%'))
        
        query = query.limit(limit).offset(offset) 
        
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
         