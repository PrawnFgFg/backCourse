


class NabronirovalExecptions(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
        
        
class ObjectNotFoundError(NabronirovalExecptions):
    detail = "Объект не найден123"
    
class AllRoomsAreBookedExecptions(NabronirovalExecptions):
    detail="Не осталось свободных номеров"
    