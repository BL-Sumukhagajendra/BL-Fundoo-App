from fastapi import HTTPException
from starlette import status

from app.models.notes import Notes
from app.repositories.note_repository import NoteRepository
from app.schemas.note_schema import NoteRequest, NoteUpdateRequest


class NoteService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def get_all_notes(self, user_id: int) -> list[Notes]:
        # Normal notes feed: not archived, not trashed
        return await self.note_repository.get_all(user_id, is_archived=False, is_trashed=False)

    async def get_trashed_notes(self, user_id: int) -> list[Notes]:
        # Trashed feed
        return await self.note_repository.get_all(user_id, is_archived=False, is_trashed=True)

    async def get_archived_notes(self, user_id: int) -> list[Notes]:
        # Archived feed
        return await self.note_repository.get_all(user_id, is_archived=True, is_trashed=False)

    async def get_note_by_id(self, note_id: int, user_id: int) -> Notes:
        note = await self.note_repository.get_by_id(note_id, user_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note

    async def search_notes(self, user_id: int, search_term: str) -> list[Notes]:
        return await self.note_repository.search(user_id, search_term)

    async def create_note(self, request: NoteRequest, user_id: int) -> Notes:
        note = Notes(
            title=request.title,
            description=request.description,
            color=request.color,
            user_id=user_id
        )
        return await self.note_repository.create(note)

    async def update_note(
        self,
        note_id: int,
        request: NoteUpdateRequest,
        user_id: int
    ) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)

        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(note, field, value)

        return await self.note_repository.update(note)

    async def move_to_trash(self, note_id: int, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.is_trashed = True
        note.is_pinned = False  # Trashed notes cannot be pinned
        return await self.note_repository.update(note)

    async def restore_from_trash(self, note_id: int, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.is_trashed = False
        return await self.note_repository.update(note)

    async def permanent_delete(self, note_id: int, user_id: int) -> None:
        note = await self.get_note_by_id(note_id, user_id)
        await self.note_repository.delete(note)

    async def archive_note(self, note_id: int, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.is_archived = True
        note.is_pinned = False  # Archived notes cannot be pinned
        return await self.note_repository.update(note)

    async def unarchive_note(self, note_id: int, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.is_archived = False
        return await self.note_repository.update(note)

    async def pin_note(self, note_id: int, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.is_pinned = True
        note.is_archived = False  # Pinned notes cannot be archived
        return await self.note_repository.update(note)

    async def unpin_note(self, note_id: int, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.is_pinned = False
        return await self.note_repository.update(note)

    async def update_color(self, note_id: int, color: str, user_id: int) -> Notes:
        note = await self.get_note_by_id(note_id, user_id)
        note.color = color
        return await self.note_repository.update(note)

    async def bulk_delete(self, note_ids: list[int], user_id: int) -> int:
        count = await self.note_repository.bulk_delete(note_ids, user_id)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No notes found to delete"
            )
        return count
