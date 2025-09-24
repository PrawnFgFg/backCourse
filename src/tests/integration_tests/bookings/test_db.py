from datetime import date

from schemas.bookings import BookingAdd, BookingUpdatePatch


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2026, month=1, day=1),
        price=100,
    )
    booking_added = await db.bookings.add(booking_data)
    
    booking_response = await db.bookings.get_one_or_none(id=booking_added.id)
    assert booking_response
    assert booking_response.id == booking_added.id
    
    booking_update_patch = BookingUpdatePatch(
        # room_id=room_id,
        # user_id=user_id,
        # date_from=date(year=2025, month=12, day=12),
        # date_to=date(year=2026, month=1, day=1),
        price=112,
        
    )
    updated_booking = await db.bookings.edit(
        schemas=booking_update_patch, 
        id=booking_response.id, 
        exclude_unset=True
        )
    
    assert updated_booking
    assert updated_booking.price == 112
    
    await db.bookings.delete(id=booking_response.id)
    booking = await db.bookings.get_one_or_none(id=booking_response.id)
    assert not booking
    
    await db.commit()
    