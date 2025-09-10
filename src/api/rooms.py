from fastapi import APIRouter, Query
from datetime import date

from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest, RoomPut
from src.schemas.facilities import RoomFacilityAdd
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
    
    r_f = [RoomFacilityAdd(rooms_id=room.id, facility_id=f_id) for f_id in create_room_schemas.facilities_ids]
    await db.room_facility.add_bulk(r_f)
    
    await db.session.commit()
    return room



@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-07-05"),
    date_to: date = Query(example="2025-10-06")
):
    rooms = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
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
    room_update: RoomPatchRequest,
    room_id: int,
):
    room_data = RoomPut(hotel_id=hotel_id, **room_update.model_dump())
    edited_room = await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    
    await db.room_facility.facility_ids_to_del_and_add(
        db=db,
        patch_schema=room_update,
        room_id=room_id,
        edited_room=edited_room,
    )
    
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
 
    await db.room_facility.facility_ids_to_del_and_add(
        db=db,
        patch_schema=patch_schema,
        room_id=room_id,
        edited_room=edited_room,
    )
    
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






        