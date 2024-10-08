import os, json, logging, base64
from fastapi import APIRouter, Query, Response
from fastapi.openapi.models import MediaType
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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
async def api_get_questions(uuid: str = Query(..., description="uuid corresponding to an interview")):
	"""
	Using the interview uuid, parses the applicant's resume, 
	and generates questions. Returns a JSON array of objects,
	each object has a "text" and "audio" field. The audio 
	field holds a base64 encoded mp4 file.
	"""
	try:
		question_audio_tuples = get_questions(uuid)
		response_data = []
		for question, audio in question_audio_tuples:
			audio.seek(0)
			audio_base64 = base64.b64encode(audio.read()).decode('utf-8')
			response_data.append({
				"text": question,
				"audioB64": audio_base64
			})
		return JSONResponse(content=response_data)
	except Exception as e:
		print(f" 💥 Error in /api/get-questions - {e}")
		return JSONResponse(content={"error":"Internal server error in get-questions"}, status_code=500)

@router.get("/api/dummy-get-questions")
async def api_dummy_get_questions(uuid: str = Query(..., description="uuid corresponding to an interview")):
	"""
	Accepts an interview uuid, returns a JSON array of objects,
	each object has a "text" and "audio" field.
	"""
	try:
		file_path = os.path.join(os.path.dirname(__file__), '../assets/SampleGetQuestionsResponse.json')
		with open(file_path, 'r') as file:
			response_data = json.load(file)

		return JSONResponse(content=response_data)

	except Exception as e:
		print(f"  Error in /api/dummy-get-questions - {e}")
		return JSONResponse(content={"error":"Internal server error in dummy-get-questions"}, status_code=500)

      
