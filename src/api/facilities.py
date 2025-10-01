from fastapi import APIRouter
from fastapi_cache.decorator import cache


from src.api.dependecies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(
    db: DBDep,
):
    return await db.facility.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_schema: FacilityAdd):
    res = await db.facility.add(schemas=facility_schema)
    await db.session.commit()

    test_task.delay()

    return {"status": "Ok", "data": res}
