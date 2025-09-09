from fastapi import APIRouter


from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd





router = APIRouter(prefix='/facilities', tags=['Удобства'])



@router.get("")
async def get_all_facilities(
    db: DBDep,
    
):
    return await db.facility.get_filtered()


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
    return res