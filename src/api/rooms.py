from fastapi import APIRouter, Query
from datetime import date

from src.database import async_session_maker
from src.repositories.rooms import RoomRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
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
    
    room_facilities_models = await db.room_facility.get_filtered(rooms_id=room_id)
    
    current_facilities = []
    for model in room_facilities_models:
        id_facility = model.model_dump()['facility_id']
        current_facilities.append(id_facility)
    
    facilities_to_add = patch_schema.model_dump().get("facilities_ids_to_add", None)
    
    if facilities_to_add:
        facility_to_add_request = []
        for fac in facilities_to_add:
            if fac not in current_facilities:
                facility_to_add_request.append(fac)
        
        models_rmfac = [RoomFacilityAdd(rooms_id=edited_room.id, facility_id=f_id) for f_id in facility_to_add_request]
        await db.room_facility.add_bulk(models_rmfac)
    
    
    facilities_to_del = patch_schema.model_dump().get("facilities_ids_to_del", None)
    if facilities_to_del:
        
        await db.room_facility.delete_bulk_for_id(room_id=room_id, ids_facilities=facilities_to_del)
    
    
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






        