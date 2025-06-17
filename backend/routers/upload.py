import os
import shutil
import traceback
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import Internship, InternshipDiscipline, Keyword
import uuid
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter()
PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
os.makedirs(PDF_DIR, exist_ok=True)  # Create uploads dir if not exists

@router.post("/upload")
async def upload_internship(
    file: UploadFile = File(...),
    start: str = Form(...),
    end: str = Form(None),
    disciplines: str = Form(...),
    title: str = Form(...),
    summary: str = Form(...),
    supervisor_id: int = Form(...),
    keywords: str = Form(None),
    db: Session = Depends(get_db)
):
    unique_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(PDF_DIR, unique_filename)
    
    with open(pdf_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    internship = Internship(
        title=title,
        summary=summary,
        start=start,
        end=end,
        pdf_path=unique_filename,
        supervisor_id=supervisor_id,
    )
    db.add(internship)
    db.commit()
    db.refresh(internship)
    
    if disciplines != None and len(disciplines) > 0:
        disciplines = disciplines.split(",")
        for discipline_id in disciplines:
            db.add(InternshipDiscipline(internship_id=internship.id, discipline_id=discipline_id))
    
    if keywords != None and len(keywords) > 0:
        keywords = keywords.split(",")
        for keyword in keywords:
            db.add(Keyword(name=keyword, internship_id=internship.id))
    
    db.commit()
    return {"message": "Internship created successfully", "id": internship.id}