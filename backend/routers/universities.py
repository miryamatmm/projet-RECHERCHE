from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import University

router = APIRouter()

@router.get("/universities")
async def get_supervisors(db: Session = Depends(get_db)):
    return db.query(University).all()
