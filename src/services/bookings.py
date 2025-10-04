from datetime import date

from fastapi import HTTPException, status

from src.services.base import BaseService
from src.api.dependecies import UserIdDep
from src.execptions import AllRoomsAreBookedException, ObjectNotFoundException, RoomNotFoundException, BookingNoteFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest

class BookingService(BaseService):
    async def create_booking(
        self,
        user_id: UserIdDep,
        data_add: BookingAddRequest,
    ):
        try:
            room_data = await self.db.rooms.get_one(id=data_add.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
            
        hotel = await self.db.hotels.get_one_or_none(id=room_data.hotel_id)
        price = room_data.model_dump().get("price")
        booking_data = BookingAdd(user_id=user_id, price=price, **data_add.model_dump())
        try:
            res = await self.db.bookings.add_booking(booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as ex:
            raise BookingNoteFoundException from ex
        await self.db.session.commit()
        return res


    async def get_all_bookings(
        self,
    ):
        bookings = await self.db.bookings.get_all()
        return bookings


    async def get_my_bookings(
        self,
        user_id: UserIdDep,
    ):
        bookings = await self.db.bookings.get_filtered(user_id=user_id)
        return bookings


    async def test(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        return await self.db.bookings.add_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)