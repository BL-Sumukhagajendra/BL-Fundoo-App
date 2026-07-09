from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["System"])

@router.get("")
async def health():
    return {"status": "healthy", "message": "Fundoo Notes API is running"}