from pydantic import BaseModel, Field



class RoomAdd(BaseModel):
    hotel_id: int
    titile: str
    description: str | None = None
    price: int 
    quantity: int
    
class Room(RoomAdd):
    pass


class RoomPatch(BaseModel):
    titile: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    
    
    
