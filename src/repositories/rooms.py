from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import NoResultFound

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import RoomsDataMapper
from src.execptions import ObjectNotFoundError



class RoomRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomsDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        # print(availavle_rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entithy(model) for model in result.scalars().unique().all()
        ]

    async def get_one_room_with_facilities(
        self,
        hotel_id: int,
        room_id: int,
    ):
        query = (
            select(RoomsORM)
            .filter_by(hotel_id=hotel_id, id=room_id)
            .options(selectinload(RoomsORM.facilities))
        )

        res = await self.session.execute(query)
        try:
            room_with_facilities = res.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundError            

        return self.mapper.map_to_domain_entithy(room_with_facilities)
