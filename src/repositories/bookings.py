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
    
    
    
        
        
    
        