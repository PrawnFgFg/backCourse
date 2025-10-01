from fastapi import APIRouter, Body, Query
from datetime import date

from fastapi_cache.decorator import cache

from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.api.dependecies import DBDep



from src.api.dependecies import PaginationDep


router = APIRouter(prefix='/hotels', tags=["Отели"])
     
    
@router.post("", summary="Добавить отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(schemas=hotel_data)
    await db.commit()
    return {"status": "Ok", "data": hotel}



@router.get('', summary="Получение отелей",
            description="Получение отелей или отеля по query параметрам")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город"),
    date_from: date = Query(example="2025-07-05"),
    date_to: date = Query(example="2025-10-06")
):
    per_page = pagination.per_page or 5
    
    return await db.hotels.get_filtered_by_time(
        date_from=date_from, 
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=pagination.page * per_page - per_page,
        )
        
        
@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep) -> Hotel:
    res = await db.hotels.get_one_or_none(id=hotel_id)
    return res



@router.put("/{hotel_id}", summary="Изменить отели полностью",)
async def put_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    edited_hotel = await db.hotels.edit(schemas=hotel_data, id=hotel_id)
    await db.commit()
    return edited_hotel




@router.patch("/{hotel_id}", summary="Изменить 1 и более параметров отеля")
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    edited_hotel = await db.hotels.edit(schemas=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return edited_hotel
    


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    res = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return res
    
    
        
 