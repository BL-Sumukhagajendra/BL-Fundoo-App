from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from app.schemas.label_schema import LabelResponse

class NoteRequest(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    description: str | None = None
    color: str | None = None

class NoteUpdateRequest(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)] | None = None
    description: str | None = None
    color: str | None = None

class ColorUpdateRequest(BaseModel):
    color: str

class BulkDeleteRequest(BaseModel):
    note_ids: list[int]

class NoteResponse(BaseModel):
    id: int
    title: str
    description: str | None
    color: str | None
    is_pinned: bool
    is_archived: bool
    is_trashed: bool
    created_at: datetime
    updated_at: datetime
    labels: list[LabelResponse] = []

    model_config = {"from_attributes": True}
