from fastapi import APIRouter


from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix='/booking', tags=["Бронирование"])


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    room_id: int,
    data_add: BookingAddRequest,
):
    room_data = await db.rooms.get_one_or_none(id=room_id)
    price = room_data.model_dump().get("price")
    booking_data = BookingAdd(user_id=user_id, price=price, **data_add.model_dump())
    res = await db.bookings.add(booking_data)
    await db.session.commit()
    return res
    