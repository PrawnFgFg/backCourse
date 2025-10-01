from fastapi import HTTPException
from sqlalchemy import select
from datetime import date

from repositories.utils import rooms_ids_for_booking
from schemas.bookings import BookingAdd
from src.models.booking import BookingOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingsDataMapper


class BookingRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingsDataMapper
    
    
    async def get_bookings_with_today_check_in(self,):
        query = (
            select(BookingOrm)
            .filter(BookingOrm.date_from == date.today())
        )
        
        res = await self.session.execute(query)
        
        return [self.mapper.map_to_domain_entithy(booking) for booking in res.scalars().all()]
    
    
    async def add_booking(
        self,
        schema_add: BookingAdd,
        hotel_id: int,
        ):
        
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=schema_add.date_from,
            date_to=schema_add.date_to,
            hotel_id=hotel_id,
        )
        
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()
        
        if schema_add.room_id in rooms_ids_to_book:
            new_booking = await self.add(schema_add)
            return new_booking
        else:
            raise HTTPException(500)
        
        
        
        
        
        
        
        
    
        