from datetime import date
from api.dependecies import PaginationDep
from execptions import check_date_to_after_date_from
from schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService



class HotelService(BaseService):
    
    async def add_hotel(
        self,
        hotel_data: HotelAdd
    ): 
        hotel = await self.db.hotels.add(schemas=hotel_data)
        await self.db.commit()
        return hotel
        
        
    async def get_hotels(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=pagination.page * per_page - per_page,
        )
        
        
    async def get_one(self, hotel_id: int):
        res = await self.db.hotels.get_one(id=hotel_id)
        
        
    async def put_hotels(self, hotel_id: int, hotel_data: HotelAdd):
        edited_hotel = await self.db.hotels.edit(schemas=hotel_data, id=hotel_id)
        await self.db.commit()
        return edited_hotel


    async def patch_hotel(
        self,
        hotel_id: int,
        hotel_data: HotelPatch,
    ):
        edited_hotel = await self.db.hotels.edit(schemas=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return edited_hotel


    async def delete_hotel(self, hotel_id: int):
        res = await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        return res

        
        
