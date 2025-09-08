from fastapi import APIRouter


from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd





router = APIRouter(prefix='/facilities', tags=['Удобства'])



@router.get("")
async def get_all_facilities(
    db: DBDep,
):
    return await db.facility.get_all()


@router.post("/")
async def create_facility(
    db: DBDep,
    facility_schema: FacilityAdd
):
    res = await db.facility.add(schemas=facility_schema)
    await db.session.commit()
    return res