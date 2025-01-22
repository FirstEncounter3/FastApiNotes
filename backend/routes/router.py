from typing import Annotated

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select

from models.models import NotePublic, NoteUpdate, NoteBase, Note
from db.db import SessionDep

router = APIRouter()
BASE_PATH = "/api/v1"


@router.get(BASE_PATH)
def hello_world():
    return RedirectResponse("/docs")


@router.post(f"{BASE_PATH}/create_notes", response_model=NotePublic)
def create_notes(note: NoteBase, session: SessionDep) -> NotePublic:
    note_instance = Note(**note.model_dump())
    session.add(note_instance)
    session.commit()
    session.refresh(note_instance)
    return note_instance


@router.get(f"{BASE_PATH}/notes", response_model=list[NotePublic])
def get_notes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[NotePublic]:
    return session.exec(select(Note).offset(offset).limit(limit)).all()


@router.get(f"{BASE_PATH}/notes/{{note_id}}", response_model=NotePublic)
def get_note_by_id(note_id: int, session: SessionDep) -> NotePublic:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.patch(f"{BASE_PATH}/notes/{{note_id}}", response_model=NotePublic)
def update_note_by_id(note_id: int, note: NoteUpdate, session: SessionDep) -> Note:
    note_to_update = session.get(Note, note_id)
    if not note_to_update:
        raise HTTPException(status_code=404, detail="Note not found")
    note_data = note.model_dump(exclude_unset=True)
    note_to_update.sqlmodel_update(note_data)
    session.add(note_to_update)
    session.commit()
    session.refresh(note_to_update)
    return note_to_update


@router.delete(f"{BASE_PATH}/notes/{{note_id}}")
def delete_note_by_id(note_id: int, session: SessionDep) -> dict:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"message": "Note successfully deleted"}
