from datetime import date

from schemas.bookings import BookingAdd, BookingUpdatePatch


async def test_add_booking(db):
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
    
    booking_update_patch = BookingUpdatePatch(
        # room_id=room_id,
        # user_id=user_id,
        # date_from=date(year=2025, month=12, day=12),
        # date_to=date(year=2026, month=1, day=1),
        price=111,
        
    )
    await db.bookings.edit(schemas=booking_update_patch, id=booking_added.id, exclude_unset=True)
    
    await db.bookings.delete(id=booking_added.id)
    
    await db.commit()
    