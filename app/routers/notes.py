from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas import NoteCreate, NoteResponse, NoteUpdate
from app.models import Note
from app.database import get_session
from datetime import datetime
from app.dependency import DBSession

router = APIRouter(prefix='/notes')

@router.post('/', response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    db: DBSession
    # db: Session = Depends(get_session)
    # db: Annotated[Session, Depends(get_session)]
):
    user_id = 1
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=user_id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get('/', response_model=list[NoteResponse])
def list_notes(db: DBSession, limit: int = 10, offset: int = 0):
    #List all notes
    stmt = select(Note).offset(offset).limit(limit)
    notes = db.exec(stmt).all()
    return notes

@router.get('/{note_id}', response_model=NoteResponse)
def get_note(note_id: int, db: DBSession):
    # Get a specific note
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Note with id {note_id} not found'
        )
    return note