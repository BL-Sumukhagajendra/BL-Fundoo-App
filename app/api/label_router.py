from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db, get_current_user
from app.models.user import User
from app.repositories.label_repository import LabelRepository
from app.services.label_service import LabelService
from app.schemas.label_schema import LabelRequest, LabelResponse

router = APIRouter(prefix="/api/labels", tags=["Labels"])

def _get_service(db: AsyncSession) -> LabelService:
    repository = LabelRepository(db)
    return LabelService(repository)

@router.get("/", response_model=list[LabelResponse])
async def get_all_labels(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.get_all_labels(current_user.id)

@router.post("/", response_model=LabelResponse, status_code=201)
async def create_label(
    request: LabelRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.create_label(request, current_user.id)

@router.put("/{labelId}", response_model=LabelResponse)
async def update_label(
    labelId: int,
    request: LabelRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.update_label(labelId, request, current_user.id)

@router.delete("/{labelId}", status_code=200)
async def delete_label(
    labelId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    await service.delete_label(labelId, current_user.id)
    return {"message": "Label deleted successfully"}
