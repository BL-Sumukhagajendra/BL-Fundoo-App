from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        default=False
    )

    # Relationships
    notes = relationship(
        "Notes",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    labels = relationship(
        "Label",
        back_populates="user",
        cascade="all, delete-orphan"
    )
