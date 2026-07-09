from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notes import Notes
from sqlalchemy import select, or_

class NoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, note_id: int, user_id: int) -> Notes | None:
        stmt = select(Notes).where(
            Notes.id == note_id, 
            Notes.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, user_id: int, is_archived: bool = False, is_trashed: bool = False) -> list[Notes]:
        stmt = select(Notes).where(
            Notes.user_id == user_id,
            Notes.is_archived == is_archived,
            Notes.is_trashed == is_trashed
        ).order_by(
            Notes.is_pinned.desc(),
            Notes.updated_at.desc()
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def search(self, user_id: int, search_term: str) -> list[Notes]:
        stmt = select(Notes).where(
            Notes.user_id == user_id,
            Notes.is_trashed == False, 
            or_(
                Notes.title.ilike(f"%{search_term}%"),
                Notes.description.ilike(f"%{search_term}%")
            )
        ).order_by(
            Notes.updated_at.desc()
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, note: Notes) -> Notes:
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def update(self, note: Notes) -> Notes:
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def delete(self, note: Notes) -> None:
        await self.db.delete(note)
        await self.db.commit()

    async def bulk_delete(self, notes_ids: list[int], user_id: int) -> int:
        stmt = select(Notes).where(
            Notes.id.in_(notes_ids),
            Notes.user_id == user_id
        )
        result = await self.db.execute(stmt)
        notes_list = list(result.scalars().all())

        for note in notes_list:
            await self.db.delete(note)

        await self.db.commit()
        return len(notes_list)
