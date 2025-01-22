from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class NoteBase(SQLModel):
    title: str = Field(max_length=100, index=True, nullable=False)
    content: str = Field(max_length=500, nullable=False)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Example Note",
                "content": "This is an example note."
            }
        }
    )


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class NotePublic(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime


class NoteUpdate(NoteBase):
    title: str | None = None
    content: str | None = None
