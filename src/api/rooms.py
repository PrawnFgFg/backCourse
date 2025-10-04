from fastapi import APIRouter, Query, HTTPException, status
from datetime import date

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, RoomPut
from src.api.dependecies import DBDep
from src.execptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, create_room_schemas: RoomAddRequest):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, create_room_schemas=create_room_schemas)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return room


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-07-05"),
    date_to: date = Query(example="2025-10-06"),
):
    return await RoomService(db).get_rooms(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
 

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    return await RoomService(db).get_one_room_by_id(hotel_id=hotel_id, room_id=room_id)



@router.put("/{hotel_id}/rooms/{room_id}")
async def put_update_room(
    db: DBDep,
    hotel_id: int,
    room_update: RoomPatchRequest,
    room_id: int,
):
    edited_room = await RoomService(db).put_update_room(
        hotel_id=hotel_id,
        room_update=room_update,
        room_id=room_id,
    )
    return edited_room


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    patch_schema: RoomPatchRequest,
):
    edited_room = await RoomService(db).patch_update_room(
        hotel_id=hotel_id,
        room_id=room_id,
        patch_schema=patch_schema,
    )
    return edited_room


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    res = await RoomService(db).delete_room_by_id(
       hotel_id=hotel_id,
       room_id=room_id, 
    )
    return res
