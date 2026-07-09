from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db, get_current_user
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.repositories.label_repository import LabelRepository
from app.services.note_service import NoteService
from app.services.label_service import LabelService
from app.schemas.note_schema import (
    NoteRequest,
    NoteUpdateRequest,
    NoteResponse,
    ColorUpdateRequest,
)

router = APIRouter(prefix="/api/notes", tags=["Notes"])

def _get_service(db: AsyncSession) -> NoteService:
    repository = NoteRepository(db)
    return NoteService(repository)

# ── 1. GET TRASHED NOTES (Must be before /{noteId}) ──
@router.get("/trash", response_model=list[NoteResponse])
async def get_trashed_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.get_trashed_notes(current_user.id)

# ── 2. GET ARCHIVED NOTES (Must be before /{noteId}) ──
@router.get("/archive", response_model=list[NoteResponse])
async def get_archived_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.get_archived_notes(current_user.id)

# ── 3. SEARCH NOTES (Must be before /{noteId}) ──
@router.get("/search", response_model=list[NoteResponse])
async def search_notes(
    search_term: Annotated[str, Query(min_length=1)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.search_notes(current_user.id, search_term)

# ── 4. GET ALL ACTIVE NOTES ──
@router.get("/", response_model=list[NoteResponse])
async def get_all_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.get_all_notes(current_user.id)

# ── 5. GET NOTE BY ID ──
@router.get("/{noteId}", response_model=NoteResponse)
async def get_note(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.get_note_by_id(noteId, current_user.id)

# ── 6. CREATE NOTE ──
@router.post("/", response_model=NoteResponse, status_code=201)
async def create_note(
    request: NoteRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.create_note(request, current_user.id)

# ── 7. UPDATE NOTE ──
@router.put("/{noteId}", response_model=NoteResponse)
async def update_note(
    noteId: int,
    request: NoteUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.update_note(noteId, request, current_user.id)

# ── 8. MOVE TO TRASH (SOFT DELETE) ──
@router.delete("/{noteId}", status_code=200)
async def move_to_trash(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    await service.move_to_trash(noteId, current_user.id)
    return {"message": "Note moved to trash"}

# ── 9. RESTORE FROM TRASH ──
@router.patch("/{noteId}/restore", response_model=NoteResponse)
async def restore_from_trash(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.restore_from_trash(noteId, current_user.id)

# ── 10. PERMANENT DELETE ──
@router.delete("/{noteId}/permanent", status_code=200)
async def permanent_delete(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    await service.permanent_delete(noteId, current_user.id)
    return {"message": "Note permanently deleted"}

# ── 11. ARCHIVE NOTE ──
@router.patch("/{noteId}/archive", response_model=NoteResponse)
async def archive_note(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.archive_note(noteId, current_user.id)

# ── 12. UNARCHIVE NOTE ──
@router.patch("/{noteId}/unarchive", response_model=NoteResponse)
async def unarchive_note(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.unarchive_note(noteId, current_user.id)

# ── 13. PIN NOTE ──
@router.patch("/{noteId}/pin", response_model=NoteResponse)
async def pin_note(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.pin_note(noteId, current_user.id)

# ── 14. UNPIN NOTE ──
@router.patch("/{noteId}/unpin", response_model=NoteResponse)
async def unpin_note(
    noteId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.unpin_note(noteId, current_user.id)

# ── 15. CHANGE COLOR ──
@router.patch("/{noteId}/color", response_model=NoteResponse)
async def update_color(
    noteId: int,
    request: ColorUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = _get_service(db)
    return await service.update_color(noteId, request.color, current_user.id)

# ── 16. ASSOCIATE LABEL ──
@router.post("/{noteId}/labels/{labelId}", response_model=NoteResponse)
async def add_label_to_note(
    noteId: int,
    labelId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    note_repo = NoteRepository(db)
    label_repo = LabelRepository(db)
    service = LabelService(label_repository=label_repo, note_repository=note_repo)
    return await service.add_label_to_note(noteId, labelId, current_user.id)

# ── 17. REMOVE LABEL ──
@router.delete("/{noteId}/labels/{labelId}", response_model=NoteResponse)
async def remove_label_from_note(
    noteId: int,
    labelId: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    note_repo = NoteRepository(db)
    label_repo = LabelRepository(db)
    service = LabelService(label_repository=label_repo, note_repository=note_repo)
    return await service.remove_label_from_note(noteId, labelId, current_user.id)
