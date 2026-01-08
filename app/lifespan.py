from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.database import MongoDB



@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    MongoDB.connect()

    print("✅ Database connected")

    yield

    # 🔹 Shutdown
    MongoDB.close()
    print("🛑 Database connection closed")
