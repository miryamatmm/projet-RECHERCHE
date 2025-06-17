from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import InternshipSupervisor

router = APIRouter()

from sqlalchemy.orm import joinedload

@router.get("/supervisors")
async def get_supervisors(db: Session = Depends(get_db)):
    return db.query(InternshipSupervisor).options(
        joinedload(InternshipSupervisor.university)  # Eager load university details
    ).all()
