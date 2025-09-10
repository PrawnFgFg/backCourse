from sqlalchemy import delete, select
from pydantic import BaseModel

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd
from src.schemas.rooms import RoomPatchRequest
from src.schemas.rooms import Room


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
        
        
    async def facility_ids_to_del_and_add(
        self,
        db,
        patch_schema: BaseModel,
        room_id: int,
        edited_room: BaseModel,
        
    ):
        room_facilities_models = await db.room_facility.get_filtered(rooms_id=room_id)
        
        models_rmfac = self.get_facilities_to_add(room_facilities_models, patch_schema, edited_room)
        if models_rmfac:
            await db.room_facility.add_bulk(models_rmfac)
        
        fac_to_del = self.get_facilities_to_del(patch_schema)
        if fac_to_del:
            await db.room_facility.delete_bulk_for_id(room_id=room_id, ids_facilities=fac_to_del)

    
    def get_facilities_to_add(
        self,
        room_facilities_models: list[RoomFacility], 
        patch_schema: RoomPatchRequest, 
        edited_room: Room,
        ):
        
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
            return models_rmfac
            
            
    def get_facilities_to_del(self, patch_schema: RoomPatchRequest):
        facilities_to_del = patch_schema.model_dump().get("facilities_ids_to_del", None)
        if facilities_to_del:
            return facilities_to_del
        
        
    