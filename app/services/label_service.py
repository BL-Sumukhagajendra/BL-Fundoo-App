from fastapi import HTTPException
from starlette import status

from app.models.label import Label
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.schemas.label_schema import LabelRequest


class LabelService:
    def __init__(self, label_repository: LabelRepository, note_repository: NoteRepository = None):
        self.label_repository = label_repository
        self.note_repository = note_repository

    async def get_all_labels(self, user_id: int) -> list[Label]:
        return await self.label_repository.get_all(user_id)

    async def get_label_by_id(self, label_id: int, user_id: int) -> Label:
        label = await self.label_repository.get_by_id(label_id, user_id)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found"
            )
        return label

    async def create_label(self, request: LabelRequest, user_id: int) -> Label:
        existing = await self.label_repository.get_by_name(request.name, user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Label with this name already exists"
            )
        label = Label(name=request.name, user_id=user_id)
        return await self.label_repository.create(label)

    async def update_label(self, label_id: int, request: LabelRequest, user_id: int) -> Label:
        label = await self.get_label_by_id(label_id, user_id)
        
        # Check if another label already has this name
        existing = await self.label_repository.get_by_name(request.name, user_id)
        if existing and existing.id != label_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another label with this name already exists"
            )
            
        label.name = request.name
        return await self.label_repository.update(label)

    async def delete_label(self, label_id: int, user_id: int) -> None:
        label = await self.get_label_by_id(label_id, user_id)
        await self.label_repository.delete(label)

    async def add_label_to_note(self, note_id: int, label_id: int, user_id: int):
        if not self.note_repository:
            raise RuntimeError("Note repository not configured")
        
        note = await self.note_repository.get_by_id(note_id, user_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

        label = await self.label_repository.get_by_id(label_id, user_id)
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")

        if label not in note.labels:
            note.labels.append(label)
            await self.note_repository.update(note)
        
        return note

    async def remove_label_from_note(self, note_id: int, label_id: int, user_id: int):
        if not self.note_repository:
            raise RuntimeError("Note repository not configured")
        
        note = await self.note_repository.get_by_id(note_id, user_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

        label = await self.label_repository.get_by_id(label_id, user_id)
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")

        if label in note.labels:
            note.labels.remove(label)
            await self.note_repository.update(note)

        return note
