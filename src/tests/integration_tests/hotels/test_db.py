

from schemas.hotels import HotelAdd
from utils.db_manager import DBManager
from src.database import async_session_maker_null_pul


async def test_add_hotel():
    hotel_data = HotelAdd(title="Сочи", location="Улица какая то1")
    async with DBManager(session_factory=async_session_maker_null_pul) as db:
        new_hote_data = await db.hotels.add(hotel_data)
        await db.commit()
        print(f'{new_hote_data=}')