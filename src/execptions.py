


from datetime import date
from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class BookingNoteFoundException(NabronirovalException):
    detail = 'Бронирование не найдено'
    
    
class RoomNotFoundException(NabronirovalException):
    detail = "Комната не найдена"
    
    
class UserAlreadyExist(NabronirovalException):
    detail = "Пользователь уже существует"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"
    

class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"
    
    
class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Такой пользователь уже существует"