from pydantic import BaseModel, Field


class RoomAddRequest(BaseModel):
    titile: str
    description: str | None = None
    price: int 
    quantity: int
    facilities_ids: list[int] | None = None
    

class RoomAdd(BaseModel):
    hotel_id: int
    titile: str
    description: str | None = None
    price: int 
    quantity: int
    
class Room(RoomAdd):
    id: int


class RoomPatchRequest(BaseModel):
    titile: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids_to_add: list[int] | None = Field(None)
    facilities_ids_to_del: list[int] | None = Field(None)
    

class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    titile: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    
    
class RoomPut(BaseModel):
    hotel_id: int
    titile: str
    description: str 
    price: int 
    quantity: int
    
    
    
