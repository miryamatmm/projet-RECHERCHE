from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text 
from routers import supervisors, upload, search, extract, universities, disciplines, download

from env import *
from database import *



# Fast API
app = FastAPI(debug=debug)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "*"
]

# Ajouter CORS (middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autorise toutes les origines.
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)


@app.get("/")
def test_db_connection(db = Depends(get_db)):
    try:
        conn = db.connection()
        conn.execute(text("SELECT 1"))  
        logger.info("Connection to database ok!")
        return {"message": "Database connection successful!"}
    except Exception as e:
        logger.error("Cant connect to DB!")
        logger.error(e)
        return {"error": str(e)}

# Inclure les routers
app.include_router(supervisors.router)
app.include_router(upload.router)
app.include_router(search.router)
app.include_router(extract.router)
app.include_router(universities.router)
app.include_router(disciplines.router)
app.include_router(download.router)
