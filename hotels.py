from fastapi import APIRouter, Body, Query
from pydantic import BaseModel
from schemas.hotels import Hotel, HotelPatch

import asyncio
import time
import aiohttp
import threading


# @app.get("/async/{i}")
# async def async_func(i: int):
#     print(f"Потоков: {threading.active_count()}")
#     print(f"Начало выполнения {i} {time.time()}")
#     await asyncio.sleep(3)
#     print(f"Конец выполнения {i} {time.time()}")
    

router = APIRouter(prefix='/hotels', tags=["Отели"])
     
            

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


class Hotel(BaseModel):
    title: str
    name: str
    
    
    

@router.post("", summary="Добавить отель")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи",
          "value": {
              "title": "Отлеь 5 звезд Сочи",
              "name": "sochi_5_stars",
          }},
    "2": {
        "summary": "Дубай",
       "value": {
           'title': "Дубай у фонтана",
           "name": "dubai_fontan",
       } 
    }
})):
    
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )
    return hotels




@router.get(
    '', 
         summary="Получение отелей",
         description="Получение отелей или отеля по query параметрам"
)
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
    page: int | None = Query(1, description="Номер страницы"),
    per_page: int | None = Query(7, description="Количество отелей на стр"),
):  
    hotels_ = []
    
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        
        hotels_.append(hotel)
    
    start = page * per_page - per_page     
    end = page * per_page 
        
    return hotels_[start:end]



@router.put("/{hotel_id}", summary="Изменить отели полностью",)
def put_hotels(hotel_id: int, hotel_data: Hotel,):
    
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        hotel["title"] = from_tuple_to_str(hotel_data.title)
        hotel['name'] = hotel_data.name
    return {"message": "Изменения применены"}




@router.patch("/{hotel_id}", summary="Изменить 1 и более параметров отеля")
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
):
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        for k,v in hotel.items(): 
            if k == "title" and hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if k == "name" and hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            
    return hotels   
        
    


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Ok"}
        
 