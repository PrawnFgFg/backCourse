from fastapi import APIRouter
from datetime import date


from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest
from src.execptions import AllRoomsAreBookedHTTPException, BookingNoteFoundException
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    data_add: BookingAddRequest,
):
    try:
        res = await BookingService(db).create_booking(user_id=user_id, data_add=data_add)
    except BookingNoteFoundException:
        raise AllRoomsAreBookedHTTPException
    return res


@router.get("/")
async def get_all_bookings(
    db: DBDep,
):
    return await BookingService(db).get_all_bookings()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await BookingService(db).get_my_bookings(user_id=user_id)


@router.get("/test")
async def test(
    db: DBDep,
    hotel_id: int,
    date_from: date,
    date_to: date,
):
    return await BookingService(db).test(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
