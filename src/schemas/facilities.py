from pydantic import BaseModel



class FacilityAdd(BaseModel):
    title: str



class Facility(BaseModel):
    
    id: int
    title: str