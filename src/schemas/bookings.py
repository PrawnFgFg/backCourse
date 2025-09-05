from pydantic import BaseModel
from datetime import date


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    
class BookingAdd(BookingAddRequest):
    user_id: int
    price: int
    
    
    
class Booking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int