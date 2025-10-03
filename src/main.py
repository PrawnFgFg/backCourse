import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.DEBUG)

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_room
from src.api.bookings import router as booking_router
from src.api.facilities import router as router_facility
from src.init import redis_manager
from src.api.images import router as router_image


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_room)
app.include_router(booking_router)
app.include_router(router_facility)
app.include_router(router_image)


@app.get("/", tags=["Начальная страница"])
def home():
    return "Helloo"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
