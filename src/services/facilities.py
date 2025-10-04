from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all_facilities(
        self,
    ):
        return await self.db.facility.get_all()


    async def create_facility(self, facility_schema: FacilityAdd):
        res = await self.db.facility.add(schemas=facility_schema)
        await self.db.session.commit()

        test_task.delay()

        return {"status": "Ok", "data": res}
