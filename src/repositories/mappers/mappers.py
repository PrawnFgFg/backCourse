from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelORM
from src.schemas.hotels import Hotel
from src.models.booking import BookingOrm
from src.models.facilities import FacilitiesORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.models.facilities import RoomsFacilitiesORM
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility
from src.schemas.rooms import Room
from src.schemas.users import User
from src.schemas.facilities import RoomFacility


class HotelDataMapper(DataMapper):
    db_model = HotelORM
    schema = Hotel
    
    
class BookingsDataMapper(DataMapper):
    db_model = BookingOrm
    schema = Booking

class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility

class RoomsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room

class UsersDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class RoomsWithRelationsDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility


