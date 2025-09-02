from fastapi import APIRouter, Body, Query, Depends
from src.schemas.hotels import Hotel, HotelPatch
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelRepository



from typing import Annotated, Any
from src.api.dependecies import PaginationDep


router = APIRouter(prefix='/hotels', tags=["Отели"])
     
    
@router.post("", summary="Добавить отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи",
          "value": {
              "title": "Велникс отель",
              "location": "Сочи, ул. Приречная, 5",
          }},
    "2": {
        "summary": "Дубай",
       "value": {
           'title': "Оникс отель",
           "location": "Дубай, ул. Моря, 10",
       } 
    }
})):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(schemas=hotel_data)
        await session.commit()
    return {"status": "Ok", "data": hotel}



@router.get('', summary="Получение отелей",
            description="Получение отелей или отеля по query параметрам")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            location=location,
            title=title,
            limit= per_page,
            offset= pagination.page * per_page - per_page,
        )
        
        
@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int) -> Hotel:
    async with async_session_maker() as session:
        res = await HotelRepository(session).get_one_or_none(id=hotel_id)
        await session.commit()
    return res



@router.put("/{hotel_id}", summary="Изменить отели полностью",)
async def put_hotels(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:      
        edited_hotel = await HotelRepository(session).edit(schemas=hotel_data, id=hotel_id)
        await session.commit()
    return edited_hotel




@router.patch("/{hotel_id}", summary="Изменить 1 и более параметров отеля")
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
):
    async with async_session_maker() as session:      
        edited_hotel = await HotelRepository(session).edit(schemas=hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return edited_hotel
    


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:  
        res = await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return res
    
    
        
 