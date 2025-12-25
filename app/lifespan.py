from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    Database.connect()
    print("✅ Database connected")

    yield

    # 🔹 Shutdown
    Database.close()
    print("🛑 Database connection closed")
