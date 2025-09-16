from fastapi import APIRouter
from schemas import RequestModel
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Here's api router."}

