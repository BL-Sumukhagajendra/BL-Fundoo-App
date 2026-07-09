from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

class LabelRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]

class LabelResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
