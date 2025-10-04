from fastapi import APIRouter
from fastapi_cache.decorator import cache


from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(
    db: DBDep,
):
    return await FacilityService(db).get_all_facilities()


@router.post("")
async def create_facility(db: DBDep, facility_schema: FacilityAdd):
    res = await FacilityService(db).create_facility(facility_schema=facility_schema)
    return {"status": "Ok", "data": res}
