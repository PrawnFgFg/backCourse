from fastapi import APIRouter
from datetime import date


from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix='/bookings', tags=["Бронирование"])


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    data_add: BookingAddRequest,
):
    room_data = await db.rooms.get_one_or_none(id=data_add.room_id)
    hotel = await db.hotels.get_one_or_none(id=room_data.hotel_id)
    price = room_data.model_dump().get("price")
    booking_data = BookingAdd(user_id=user_id, price=price, **data_add.model_dump())
    res = await db.bookings.add_booking(booking_data, hotel_id=hotel.id)
    await db.session.commit()
    return res


@router.get("/")
async def get_all_bookings(
    db: DBDep,
):
    bookings = await db.bookings.get_all()
    return bookings


@router.get('/me')
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