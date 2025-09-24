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
    

class BookingUpdatePatch(BaseModel):
    room_id: int | None = None 
    user_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None
    