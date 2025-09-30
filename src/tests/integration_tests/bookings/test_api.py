import pytest
from sqlalchemy import delete


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-01-01", "2025-01-10", 200),
    (1, "2025-01-02", "2025-01-11", 200),
    (1, "2025-01-03", "2025-01-12", 200),
    (1, "2025-01-04", "2025-01-13", 200),
    (1, "2025-01-05", "2025-01-14", 200),
    (1, "2025-01-06", "2025-01-15", 500),
    (1, "2025-01-22", "2025-01-23", 200),
    (1, "2025-01-22", "2025-01-28", 200),
    
    
])
async def test_add_booking(
    room_id, date_from, date_to, status_code, 
    db, authenticated_ac):
    
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    
    assert response.status_code == status_code
    if status_code == 200:
        assert isinstance(response.json(), dict)



@pytest.fixture(scope="function")
async def test_delete_all_bookings(db):
    if not hasattr(test_add_and_get_bookings, "_executed"):
        stmt = delete(db.bookings.mapper.db_model)
        res = await db.session.execute(stmt)
        await db.commit()
        test_add_and_get_bookings._executed = True


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, count", [
    (1, "2025-01-01", "2025-01-10", 200, 1),
    (1, "2025-01-02", "2025-01-11", 200, 2),
    (1, "2025-01-03", "2025-01-12", 200, 3),
])
async def test_add_and_get_bookings(
    test_delete_all_bookings,
    db,
    authenticated_ac,
    room_id, date_from, date_to, status_code
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    if response.status_code == status_code:
        assert isinstance(response.json(), dict)
    
    response_me = await authenticated_ac.get(
        "/bookings/me"
    )
    
    assert isinstance(response_me.json(), list)

