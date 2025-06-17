from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import Discipline

router = APIRouter()

@router.get("/disciplines")
async def get_supervisors(db: Session = Depends(get_db)):
    return db.query(Discipline).all()
