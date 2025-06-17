import os
import shutil
import traceback
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse

router = APIRouter()
PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
os.makedirs(PDF_DIR, exist_ok=True)  # Create uploads dir if not exists

@router.get("/download/{pdf_filename}")
async def download_pdf(pdf_filename: str):
    file_path = os.path.join(PDF_DIR, pdf_filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path, media_type="application/pdf", filename=pdf_filename)