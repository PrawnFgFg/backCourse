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


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        

        
    
        
        
@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "lalaka@march.com",
                'password': "1234"
            }
        )

