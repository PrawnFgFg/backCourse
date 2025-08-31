from fastapi import APIRouter, Body, Query, Depends
from sqlalchemy import insert, select, any_, or_

from src.schemas.hotels import Hotel, HotelPatch
from src.database import async_session_maker, engine
from src.models.hotels import HotelORM



from typing import Annotated
from src.api.dependecies import PaginationDep



# @app.get("/async/{i}")
# async def async_func(i: int):
#     print(f"Потоков: {threading.active_count()}")
#     print(f"Начало выполнения {i} {time.time()}")
#     await asyncio.sleep(3)
#     print(f"Конец выполнения {i} {time.time()}")
    

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
        add_hotel_stmt = insert(HotelORM).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
        return {'status': "OK"}
    
    




@router.get(
        '', 
         summary="Получение отелей",
         description="Получение отелей или отеля по query параметрам"
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город"),
):  
    per_page = pagination.per_page or 5 
    search_values = ["Велникс", "Оникс"]
    async with async_session_maker() as session:
        query = select(HotelORM)
        
        if location:
            query = query.filter(HotelORM.location.ilike(f'{location}%'))
        if title:   
            query = query.filter(HotelORM.title.ilike(f"{title}%"))
        query = (
            query
            .limit(per_page)
            .offset(pagination.page * per_page - per_page)
        )    
            
        result = await session.execute(query)
        hotels = result.scalars().all()
        
        return hotels



@router.put("/{hotel_id}", summary="Изменить отели полностью",)
def put_hotels(hotel_id: int, hotel_data: Hotel,):
    
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        hotel["title"] = hotel_data.title
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
        
 