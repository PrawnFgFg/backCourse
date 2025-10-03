from fastapi import APIRouter, HTTPException, status
from datetime import date


from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.execptions import AllRoomsAreBookedException, RoomNotFoundHTTPException, ObjectNotFoundException

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    data_add: BookingAddRequest,
):
    try:
        room_data = await db.rooms.get_one(id=data_add.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер не существует")
        
    hotel = await db.hotels.get_one_or_none(id=room_data.hotel_id)
    price = room_data.model_dump().get("price")
    booking_data = BookingAdd(user_id=user_id, price=price, **data_add.model_dump())
    try:
        res = await db.bookings.add_booking(booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Не осталось свободных номеров")
    await db.session.commit()
    return res


@router.get("/")
async def get_all_bookings(
    db: DBDep,
):
    bookings = await db.bookings.get_all()
    return bookings


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.get("/test")
async def test(
    db: DBDep,
    hotel_id: int,
    date_from: date,
    date_to: date,
):
    return await db.bookings.add_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
