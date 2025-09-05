from pydantic import BaseModel, Field


class RoomAddRequest(BaseModel):
    titile: str
    description: str | None = None
    price: int 
    quantity: int
    

class RoomAdd(BaseModel):
    hotel_id: int
    titile: str
    description: str | None = None
    price: int 
    quantity: int
    
class Room(RoomAdd):
    pass


class RoomPatchRequest(BaseModel):
    titile: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    

class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    titile: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    
    
    
