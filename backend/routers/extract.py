from fastapi import FastAPI, APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from env import *
from database import get_db
from models import Discipline
from datetime import datetime

router = APIRouter()

# Endpoint to automatically extract critical data from PDF

if not qwen_enabled:
    @router.post("/extract")
    async def extract_pdf(file: UploadFile = File(...)):
        return {
            "title": "",
            "summary": "",
            "start": "01-" + datetime.now().strftime("%m-%Y"),
            "end": None,
            "dates": "[]",
            "disciplines": [],
            "keywords": []
        }
else:
    import time
    import re
    from io import BytesIO
    import PyPDF2
    from mdclense.parser import MarkdownParser
    import json

    def remove_surrounding_quotes(text):
        if text.startswith('"') and text.endswith('"'):
            return text[1:-1]
        return text

    def remove_markdown(text):
        parser = MarkdownParser()
        return parser.parse(text)
    
    def clean_response(text):
        return remove_surrounding_quotes(remove_markdown(text))
    
    def clean_json(response: str):
        """Attempts to clean and parse JSON string, or returns the original response if not valid JSON."""
        try:
            return json.loads(remove_markdown(response))
        except json.JSONDecodeError as e:
            logger.error("JSON ERRROR")
            logger.error(f"<{response}>")
            return response.strip()
    
    def ensure_trailing_dot(text):
        return text if text.endswith('.') else text + '.'

    def extract_text_from_pdf(file: UploadFile):
        """Improved text extraction with PDF formatting cleanup"""
        text = ""
        pdf_reader = PyPDF2.PdfReader(BytesIO(file.file.read()))
        for page_num in range(min(len(pdf_reader.pages), 4)):  # Limit to 4 pages
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        # Clean up PDF artifacts
        text = re.sub(r'-\n(\w)', r'\1', text)  # Join hyphenated words
        text = re.sub(r'\s+', ' ', text)        # Remove extra whitespace
        text = re.sub(r'\s([?.!](?:\s|$))', r'\1', text)  # Fix spacing before punctuation
        return text.strip()[:15000]  # Limit to ~4 pages


    CHAT_SERVER_URL = "http://localhost:8888"
    import requests

    @router.post("/extract")
    async def extract_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
        job_offer_text = extract_text_from_pdf(file)
        questions = [
            ("title",     "Give a short title for this job offer, answer only the exact title: " + job_offer_text),
            ("summary",   "Summarize this job offer in exactly two sentences: "),
            ("dates",     """Extract start and end month/year of this offer as a JSON pair like ["MM-YYYY", "MM-YYYY"]: """),
            ("disciplines",  """List all scientific subdisciplines of this offer as a JSON list like ["Domain1", "SubDomain1", "Domain2" ... ]: """),
            ("keywords",  """Find cool keywords that would help to find this job offer, reply as a JSON list like ["Plants", "Laboratory", "Outdoor"... ]: """ + job_offer_text),
        ]
        
        session_response = requests.post(f"{CHAT_SERVER_URL}/start_session")
        session_id = session_response.json().get("session_id")

        if not session_id:
            return {"error": "Failed to create chat session"}
        
        response_data = {}
        
        ts = time.time()
        for question_type, question in questions:
            chat_response = requests.post(
                f"{CHAT_SERVER_URL}/chat", 
                json={"session_id": session_id, "message": question}
            )
            
            if chat_response.status_code != 200:
                return {"error": "Chat server error"}
            
            response = chat_response.json().get("response", "").strip()
            
            if question_type == 'title':
                response = clean_response(response)
            elif question_type == 'summary':
                response = ensure_trailing_dot(clean_response(response))
            elif question_type == 'keywords':
                response = clean_json(clean_response(response))
            elif question_type == 'disciplines':
                response = clean_json(response)  # should be a JSON string already
                keywords = db.query(Discipline).all()
                # Get existing discipline names from database
                existing_disciplines = [(d.id, d.name) for d in keywords]
                
                response_data["disciplines"] = []

                # Loop over each generated keyword
                for keyword in response:
                    # Create prompt to map the current keyword to the closest existing discipline
                    mapping_prompt = f"""
                    You are tasked with mapping a 'Generated discipline' to some 'Existing discipline name' only if some are really matching. Return only a JSON-formatted list of integers representing the IDs of the matched disciplines. The output must be a flat list (e.g., [1, 2], not [[1, 2]]). If no match is found, return an empty list ([]).

                    Generated discipline: {repr(keyword)}
                    Existing discipline names (ID, Name): {existing_disciplines}"""
                    
                    # Get mapped keyword from LLM
                    map_response = requests.post(
                        f"{CHAT_SERVER_URL}/chat",
                        json={"session_id": session_id, "message": mapping_prompt}
                    )

                    if map_response.status_code == 200:
                        mapped = clean_json(map_response.json().get("response", ""))
                        logger.debug("mapped is : ")
                        logger.debug(mapped)
                        logger.debug("---")
                        if isinstance(mapped, list):  # Validate response format
                            response_data["disciplines"].extend(mapped)
                        else:
                            logger.error("Invalid mapped keyword format")
                    else:
                        logger.error("Keyword mapping request failed")

                response = response_data["disciplines"]
                
                #response_data[question_type] = response                
            elif question_type == 'dates':
                jsonDates = clean_json(response)
                response_data['start'] =  None if len(jsonDates) < 1 else '01-' + jsonDates[0]
                response_data['end'] = None if len(jsonDates) < 2 else '01-' + jsonDates[1]
                
            else:
                logger.error("Unknown question type!")
            
            response_data[question_type] = response
        
        logger.debug(f"\nLLM PDF processing duration: {time.time() - ts} seconds")
        return response_data
