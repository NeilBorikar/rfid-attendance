from fastapi import APIRouter
from core.database import MongoDB

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    MongoDB.get_database()
    return {"status": "OK"}
