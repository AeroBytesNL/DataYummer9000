from fastapi import APIRouter, Depends
from api.auth import verify_api_key

router = APIRouter()

@router.get("/secure-data/", dependencies=[Depends(verify_api_key)])
async def secure_data():
    return {"message": "success"}