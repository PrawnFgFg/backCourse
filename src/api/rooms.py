from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.rooms import RoomRepository
from src.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix='/hotels', tags=["Номера"])



@router.post('/{hotel_id}/rooms')
async def create_room(
    hotel_id: int,
    create_room_schemas: RoomAdd
):
    async with async_session_maker() as session:
        room = await RoomRepository(session).add(schemas=create_room_schemas)
        await session.commit()
    return room



@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int
):
    async with async_session_maker() as session:
        rooms = await RoomRepository(session).get_all()
        await session.commit()
    return rooms


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_one_room_by_id(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        room = await RoomRepository(session).get_one_or_none(id=room_id)
        await session.commit()
    return room


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_update_room(
    hotel_id: int,
    room_update: RoomPatch,
    room_id: int,
):
    async with async_session_maker() as session:
        edited_room = await RoomRepository(session).edit(room_update, id=room_id)
        await session.commit()
    return edited_room


@router.patch('/{hotel_id}/rooms/{room_id}')
async def patch_update_room(
    hotel_id: int,
    room_id: int,
    patch_schema: RoomPatch,
):
    async with async_session_maker() as session:
        edited_room = await RoomRepository(session).edit(patch_schema, id=room_id, exclude_unset=True)
        await session.commit()
    return edited_room


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room_by_id(
    room_id: int
):
    async with async_session_maker() as session:
        res = await RoomRepository(session).delete(id=room_id)
        await session.commit()
    return res






        