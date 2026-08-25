from api.auth_router import router as auth_router
from api.location_router import router as location_router
from api.booking_router import router as booking_router
from api.workspace_router import router as workspace_router
from api.tariff_router import router as tariff_router
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from clients.database.connection import init_pool

db_pool: asyncpg.Pool = None 

@asynccontextmanager
async def lifespan(app):
    await init_pool()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(location_router)
app.include_router(booking_router)
app.include_router(workspace_router)
app.include_router(tariff_router)
