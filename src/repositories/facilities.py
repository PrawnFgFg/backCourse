from sqlalchemy import delete, select, insert
from pydantic import BaseModel

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import RoomFacilityAdd
from src.repositories.mappers.mappers import FacilitiesDataMapper, RoomsWithRelationsDataMapper


class FacilityRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesDataMapper


class RoomFacilityRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomsWithRelationsDataMapper

    async def set_facilities_ids(self, room_id: int, facilities_ids: list[int]):
        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(
            rooms_id=room_id
        )

        res = await self.session.execute(get_current_facilities_ids_query)
        curretn_facilities: list[int] = res.scalars().all()

        faiclities_ids_to_insert = list(set(facilities_ids) - set(curretn_facilities))
        facilities_ids_to_del = list(set(curretn_facilities) - set(facilities_ids))

        facilities_rooms_to_add: list[BaseModel] = [
            RoomFacilityAdd(rooms_id=room_id, facility_id=f_id) for f_id in faiclities_ids_to_insert
        ]

        if facilities_rooms_to_add:
            m2m_facit_rooms_add_stmt = insert(RoomsFacilitiesORM).values(
                [{"rooms_id": room_id, "facility_id": f_id} for f_id in faiclities_ids_to_insert]
            )

            await self.session.execute(m2m_facit_rooms_add_stmt)

        if facilities_ids_to_del:
            m2m_facit_rooms_del_stmt = delete(RoomsFacilitiesORM).filter(
                RoomsFacilitiesORM.rooms_id == room_id,
                RoomsFacilitiesORM.facility_id.in_(facilities_ids_to_del),
            )

            await self.session.execute(m2m_facit_rooms_del_stmt)
