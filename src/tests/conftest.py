# from typing import AsyncGenerator
from pydantic import BaseModel
import pytest
from httpx import ASGITransport, AsyncClient
import json

from src.config import settings
from src.database import engine_null_pool, Base, async_session_maker_null_pul
from src.models import *
from src.main import app
from src.utils.db_manager import DBManager
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    print("Я ФИКСТУРА")
    assert settings.MODE == "TEST"
    
    
    
@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pul) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        
@pytest.fixture(scope='session', autouse=True)
async def add_hotels_and_rooms(setup_database):
    
    with open("src/tests/mock_hotels.json", "r", encoding="utf-8") as file_hotels:
        hotels: list[dict] = json.load(file_hotels)
        
    with open("src/tests/mock_rooms.json", "r", encoding="utf-8") as file_rooms:
        rooms: list[dict] = json.load(file_rooms)
    
    hotel_add: list[BaseModel] = [HotelAdd(**schema) for schema in hotels]
    rooms_add: list[BaseModel] = [RoomAdd(**data) for data in rooms]
    
    async with DBManager(session_factory=async_session_maker_null_pul) as db_:
        await db_.hotels.add_bulk(data=hotel_add)
        await db_.rooms.add_bulk(data=rooms_add)
        await db_.commit()
        

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
        
        
@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "lalaka@march.com",
            'password': "1234"
        }
    )

