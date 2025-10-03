from fastapi import APIRouter, Body, Query, HTTPException, status
from datetime import date

from fastapi_cache.decorator import cache

from src.services.hotels import HotelService
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.api.dependecies import DBDep
from src.execptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException


from src.api.dependecies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.post("", summary="Добавить отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Велникс отель",
                    "location": "Сочи, ул. Приречная, 5",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Оникс отель",
                    "location": "Дубай, ул. Моря, 10",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "Ok", "data": hotel}


@router.get(
    "", summary="Получение отелей", description="Получение отелей или отеля по query параметрам"
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город"),
    date_from: date = Query(example="2025-07-05"),
    date_to: date = Query(example="2025-10-06"),
):
    return await HotelService(db).get_hotels(
            pagination=pagination,
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
        )


@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep) -> Hotel:
    try:
        res = await HotelService(db).get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return res


@router.put(
    "/{hotel_id}",
    summary="Изменить отели полностью",
)
async def put_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    edited_hotel = HotelService(db).put_hotels(hotel_data, hotel_id=hotel_id)
    return edited_hotel


@router.patch("/{hotel_id}", summary="Изменить 1 и более параметров отеля")
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    edited_hotel = await HotelService(db).patch_hotel(hotel_data=hotel_data, hotel_id=hotel_id)
    return edited_hotel


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    res = await HotelService(db).delete_hotel(hotel_id=hotel_id)
    return res
