from pydantic import BaseModel
from sqlalchemy import func, select, insert
from datetime import date

from repositories.utils import rooms_ids_for_booking
from src.models.booking import BookingOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingsDataMapper
from src.models.rooms import RoomsORM


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
        schema_add: BaseModel,
        room_id: int,
        ):
        
        count_booked_rooms_for_current_hotel = (
            select(BookingOrm.room_id, func.count("*").label("counta"))
            .select_from(BookingOrm)
            .where(room_id == BookingOrm.room_id)
            .group_by(BookingOrm.room_id)
            .cte(name="count_booked_rooms_for_current_hotel")
        )
    
     
        upper_and_rooms = (
            select(RoomsORM, (count_booked_rooms_for_current_hotel.c.counta).label("counta"))
            .join(
                count_booked_rooms_for_current_hotel, 
                RoomsORM.id == count_booked_rooms_for_current_hotel.c.room_id
                )
            .cte(name="upper_and_rooms")
        )
        
        
        
        all_count_and_booked_rooms = (
            select(
                upper_and_rooms.c.id, 
                upper_and_rooms.c.quantity, 
                ((upper_and_rooms.c.counta).label("counta"))
                   )
            .cte(name="all_count_and_booked_rooms")
        )
        
        query = (
            select(all_count_and_booked_rooms.c.quantity - all_count_and_booked_rooms.c.counta)
        )
        
        res = await self.session.execute(query)
        available_count = res.scalars().one_or_none()
        
        if available_count <= 0 or available_count is None:
            raise Exception("Номеров больше нет")
        
        return await self.add(schemas=schema_add)
        
        
    
        