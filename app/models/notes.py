from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, func
from datetime import datetime
from app.core.database import Base

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    color: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )
    is_pinned: Mapped[bool] = mapped_column(
        default=False
    )
    is_archived: Mapped[bool] = mapped_column(
        default=False
    )
    is_trashed: Mapped[bool] = mapped_column(
        default=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="notes")
    labels = relationship("Label", secondary="note_labels", back_populates="notes", lazy="selectin")
