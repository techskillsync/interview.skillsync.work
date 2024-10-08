import os
from fastapi import APIRouter, Query
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
import logging

from api.utils.GetAudio import GetAudio
from services.GetQuestions import get_questions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def home():
	return "I am an interviewer API. Hello :p"

class api_get_audio_request(BaseModel):
    question: str

@router.get("/api/get-questions")
async def api_get_questions():
	"""
	Using the interview uuid, parses the applicant's resume, 
	and generates questions. Returns the question text and audio
	in the response body.
	"""
	try:
		raise Exception("Not implemented yet, use dummy endpoint")
	except Exception as e:
		print(f" 💥 Error in /api/get-questions - {e}")
		return JSONResponse(content={"error":"Internal server error in get-questions"}, status_code=500)

@router.get("/api/dummy-get-questions")
async def api_dummy_get_questions(uuid: str = Query(..., description="uuid corresponding to an interview")):
	"""
	Accepts an interview uuid, returns sample questions and
	audio.
	"""
	try:
		get_questions(uuid)
		raise Exception("Not implemented yet")
	except Exception as e:
		print(f"  Error in /api/dummy-get-questions - {e}")
		return JSONResponse(content={"error":"Internal server error in dummy-get-questions"}, status_code=500)

      
