from sqlalchemy import delete, select

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilityRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility
    
    
class RoomFacilityRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility
    
    
    async def delete_bulk_for_id(
        self,
        room_id: int,
        ids_facilities: list[int],
    ):
        get_id_to_del_stmt = (
            select(RoomsFacilitiesORM.facility_id)
            .select_from(RoomsFacilitiesORM)
            .filter(RoomsFacilitiesORM.facility_id.in_(ids_facilities))
        )
        
        
        delete_stmt = delete(RoomsFacilitiesORM).filter(RoomsFacilitiesORM.facility_id.in_(get_id_to_del_stmt))
        await self.session.execute(delete_stmt)