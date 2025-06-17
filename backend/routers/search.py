from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models import Internship, InternshipDiscipline, InternshipSupervisor
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import or_, and_, func
from models import Internship, Keyword, InternshipDiscipline, InternshipSupervisor, Discipline, SupervisorRoleEnum
from database import get_db
import os
from env import *
import requests

router = APIRouter()


PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
os.makedirs(PDF_DIR, exist_ok=True)

FASTAPI_SEARCH_URL = "http://localhost:8889/search"


# Endpoint to search internships

from sqlalchemy.orm import joinedload

@router.get("/search")
def search_internships(
    db: Session = Depends(get_db),
#    query: Optional[str] = None,
    keywords: Optional[List[str]] = Query(None),
    discipline_ids: Optional[List[int]] = Query(None),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    university_id: Optional[int] = None,
    supervisor_role: Optional[SupervisorRoleEnum] = None,
    page: int = 1,  # Default page is 1
    page_size: int = 10,  # Default page size is 10
):
    page_size = 10 # hardcoding page size hor now, later we may let users change it.
    
    # Base query with necessary joins
    q = db.query(Internship).options(
        joinedload(Internship.keywords),
        joinedload(Internship.disciplines).joinedload(InternshipDiscipline.discipline),
        joinedload(Internship.supervisor).joinedload(InternshipSupervisor.university)
    ).join(Internship.supervisor)
    
    import json
    
            
    if keywords is not None:
        biobert_ids = []
        if biobert_enabled:
            response = requests.get(FASTAPI_SEARCH_URL, params={"queries": keywords})
        
            if response.status_code != 200:
                logger.warning(response.text)
                logger.warning("Failed to fetch results from search server")
            else:
                logger.warning(response.text)
                search_results = response.json()
                all_pdf_paths = []
                for query in search_results:
                    print("-------dwawadaw", query)
                    if len(query['results']):
                        for result in query['results']:
                            all_pdf_paths.extend(result[0].replace('../uploads/', '') for result in query['results'])
                biobert_ids = db.query(Internship.id).where(Internship.pdf_path.in_(all_pdf_paths)).all()
                biobert_ids = [x[0] for x in biobert_ids]
        for keyword in keywords:
            res = (db.query(Internship.id).join(Keyword).filter(Keyword.name.ilike(f"%{keyword}%")).all())#filter(Keyword.name.ilike(keyword)).all())
            res = [x[0] for x in res]
            q = q.filter(or_(
                Internship.title.ilike(f"%{keyword}%"),
                Internship.summary.ilike(f"%{keyword}%"),
                Internship.id.in_(res),
                Internship.id.in_(biobert_ids)
            ))

    # Discipline hierarchy handling
    if discipline_ids:
        cte = (
            db.query(Discipline.id)
            .filter(Discipline.id.in_(discipline_ids))
            .cte(recursive=True)
        )
        d = aliased(Discipline)
        cte = cte.union_all(db.query(d.id).filter(d.parent_id == cte.c.id))
        discipline_subquery = db.query(cte.c.id).distinct().subquery()
        q = q.join(InternshipDiscipline).join(
            discipline_subquery, 
            InternshipDiscipline.discipline_id == discipline_subquery.c.id
        )

    # Date range filtering
    if start_date is not None and end_date is not None:
        q = q.filter(
            Internship.start <= end_date,
            or_(Internship.end >= start_date, Internship.end.is_(None))
        )
    elif start_date is not None:
        q = q.filter(Internship.start >= start_date)
    elif end_date is not None:
        q = q.filter(or_(Internship.end <= end_date, Internship.end.is_(None)))

    # University filter
    if university_id and str(university_id) != '-1':
        q = q.filter(InternshipSupervisor.university_id == university_id)

    # Supervisor role filter
    if supervisor_role:
        q = q.filter(InternshipSupervisor.role == supervisor_role)

    # Pagination logic
    total_count = q.distinct().count()  # Get the total count of records
    q = q.offset((page - 1) * page_size).limit(page_size)  # Apply pagination

    results = q.all()

    return {
        "data": results,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_count + page_size - 1) // page_size  # Calculate total pages
    }


@router.get("/posted_by")
def get_my_internships(supervisor_id: int, db: Session = Depends(get_db)):
    results = db.query(Internship).options(
        joinedload(Internship.keywords), 
        joinedload(Internship.disciplines).joinedload(InternshipDiscipline.discipline),
        joinedload(Internship.supervisor).joinedload(InternshipSupervisor.university)  # Load supervisor & university
    ).filter(Internship.supervisor_id == supervisor_id).all()  # Filter by supervisor_id
    
    return results

@router.get("/delete")
def delete_internship(internship_id: int, db: Session = Depends(get_db)):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    db.delete(internship)
    db.commit()
    
    return {"message": "Internship deleted successfully"}
