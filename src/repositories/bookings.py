from pydantic import BaseModel

from src.models.booking import BookingOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking



class BookingRepository(BaseRepository):
    model = BookingOrm
    schema: BaseModel= Booking