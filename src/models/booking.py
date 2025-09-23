from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import date

from src.database import Base


class BookingOrm(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int] 
    
    @property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days