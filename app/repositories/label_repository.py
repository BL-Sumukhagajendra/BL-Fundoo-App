from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.label import Label

class LabelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, label_id: int, user_id: int) -> Label | None:
        stmt = select(Label).where(
            Label.id == label_id,
            Label.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, user_id: int) -> list[Label]:
        stmt = select(Label).where(Label.user_id == user_id).order_by(Label.name.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_name(self, name: str, user_id: int) -> Label | None:
        stmt = select(Label).where(
            Label.name == name,
            Label.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, label: Label) -> Label:
        self.db.add(label)
        await self.db.commit()
        await self.db.refresh(label)
        return label

    async def update(self, label: Label) -> Label:
        await self.db.commit()
        await self.db.refresh(label)
        return label

    async def delete(self, label: Label) -> None:
        await self.db.delete(label)
        await self.db.commit()
