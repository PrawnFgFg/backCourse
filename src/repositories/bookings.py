from sqlalchemy import select
from datetime import date

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