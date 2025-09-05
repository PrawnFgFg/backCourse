from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.rooms import RoomRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.dependecies import DBDep

router = APIRouter(prefix='/hotels', tags=["Номера"])



@router.post('/{hotel_id}/rooms')
async def create_room(
    db: DBDep,
    hotel_id: int,
    create_room_schemas: RoomAddRequest
):
    room_data = RoomAdd(hotel_id=hotel_id, **create_room_schemas.model_dump())
    room = await db.rooms.add(schemas=room_data)
    await db.session.commit()
    return room



@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int
):
    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)
    return rooms


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_one_room_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return room


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_update_room(
    db: DBDep,
    hotel_id: int,
    room_update: RoomAddRequest,
    room_id: int,
):
    room_data = RoomAdd(hotel_id=hotel_id, **room_update.model_dump())
    edited_room = await db.rooms.edit(room_update, id=room_id, hotel_id=hotel_id)
    await db.session.commit()
    return edited_room


@router.patch('/{hotel_id}/rooms/{room_id}')
async def patch_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    patch_schema: RoomPatchRequest,
):
    room_data = RoomPatch(hotel_id=hotel_id, **patch_schema.model_dump(exclude_unset=True))
    edited_room = await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    await db.session.commit()
    return edited_room


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    res = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.session.commit()
    return res






        