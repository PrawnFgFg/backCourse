from fastapi import APIRouter
import json

from fastapi_cache.decorator import cache


from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd
from src.init import redis_manager
from src.tasks.tasks import test_task




router = APIRouter(prefix='/facilities', tags=['Удобства'])



@router.get("")
# @cache(expire=10)
async def get_all_facilities(
    db: DBDep,
):
    return await db.facility.get_all()
  
        


@router.get('/{room_id}')
async def gggg(
    db: DBDep,
    room_id: int,
):
    res = await db.room_facility.delete_bulk_for_id(room_id=room_id, ids_facilities=[1, 2])
    print(res)


@router.post("/")
async def create_facility(
    db: DBDep,
    facility_schema: FacilityAdd
):
    res = await db.facility.add(schemas=facility_schema)
    await db.session.commit()
    
    test_task.delay()
    
    return res