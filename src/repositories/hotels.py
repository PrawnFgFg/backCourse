from src.repositories.base import BaseRepository
from src.models.hotels import HotelORM
from src.schemas.hotels import Hotel
from sqlalchemy import select
from pydantic import BaseModel


class HotelRepository(BaseRepository):
    model = HotelORM
    schema: BaseModel = Hotel
    
    async def get_all(
        self,
        location: str | None = None,
        title: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        id: int | None = None,
    ):
    
        query = select(HotelORM)
        
        if location:
            query = query.filter(HotelORM.location.ilike(f'%{location.strip()}%'))
        if title:   
            query = query.filter(HotelORM.title.ilike(f"%{title.strip()}%"))
        if id:
            query = query.filter_by(id=id)            
        query = (
            query
            .limit(limit)
            .offset(offset)
        )    
            
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        