from datetime import date

from fastapi import Query
from src.execptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    check_date_to_after_date_from,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest, RoomPut
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def create_room(self, hotel_id: int, create_room_schemas: RoomAddRequest):
        room_data = RoomAdd(hotel_id=hotel_id, **create_room_schemas.model_dump())
        try:
            room = await self.db.rooms.add(schemas=room_data)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundHTTPException from ex
        r_f = [
            RoomFacilityAdd(rooms_id=room.id, facility_id=f_id)
            for f_id in create_room_schemas.facilities_ids
        ]
        if r_f:
            await self.db.room_facility.add_bulk(r_f)

        await self.db.commit()
        return room

    async def get_rooms(
        self,
        hotel_id: int,
        date_from: date = Query(example="2025-07-05"),
        date_to: date = Query(example="2025-10-06"),
    ):
        check_date_to_after_date_from(date_from=date_from, date_to=date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_one_room_by_id(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one_room_with_facilities(room_id=room_id, hotel_id=hotel_id)
        if not room:
            raise HotelNotFoundHTTPException
        return room

    async def put_update_room(
        self,
        hotel_id: int,
        room_update: RoomPatchRequest,
        room_id: int,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(room_id=room_id)

        room_data = RoomPut(hotel_id=hotel_id, **room_update.model_dump())
        edited_room = await self.db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
        await self.db.room_facility.set_facilities_ids(
            room_id=room_id, facilities_ids=room_update.facilities_ids
        )

        await self.db.session.commit()
        return edited_room

    async def patch_update_room(
        self,
        hotel_id: int,
        room_id: int,
        patch_schema: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(room_id=room_id)

        patch_schema_dict = patch_schema.model_dump(exclude_unset=True)
        room_data = RoomPatch(hotel_id=hotel_id, **patch_schema_dict)
        edited_room = await self.db.rooms.edit(
            room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True
        )

        if "facilities_ids" in patch_schema_dict:
            await self.db.room_facility.set_facilities_ids(
                room_id=room_id, facilities_ids=patch_schema_dict["facilities_ids"]
            )

        await self.db.session.commit()
        return edited_room

    async def delete_room_by_id(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(room_id=room_id)

        res = await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.session.commit()
        return res

    async def get_room_with_check(self, room_id: int):
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException
