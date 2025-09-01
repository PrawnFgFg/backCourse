from src.repositories.base import BaseRepository
from src.models.hotels import HotelORM
from sqlalchemy import select


class HotelRepository(BaseRepository):
    model = HotelORM
    
    async def get_all(
        self,
        location: str | None = None,
        title: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        id: int | None = None,
    ):
        # per_page = pagination.per_page or 5 
    
    
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
        return result.scalars().all()
        