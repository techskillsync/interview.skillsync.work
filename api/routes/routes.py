import os
from fastapi import APIRouter, Body, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import Response, StreamingResponse, JSONResponse
import logging

from services.GetAudio import GetAudio
from services.SpeechAnalysis import analyze_sentiment
from services.Video2Text import process_video_bytes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def home():
	return "I am an interviewer API. Hello :p"

class api_get_audio_request(BaseModel):
    question: str

@router.post("/api/get-audio")
async def api_get_audio(request: api_get_audio_request):
	"""
	Returns the question read aloud in the form of a BytesIO file.
	"""
	try:
		raise Exception("Use dummy api, we runnin out of tokens!")
		audio = GetAudio(request.question)

		return StreamingResponse(audio, media_type="audio/mpeg")
	except Exception as e:
		print(f" 💥 Error in /api/get-audio - {e}")
		return JSONResponse(content={"error":"Internal server error"}, status_code=500)


@router.post("/api/get-audio-dummy")
async def api_get_audio_dummy(request: api_get_audio_request):
	"""
	Returns a saved version of a question being read aloud.
	"""
	DUMMY_AUDIO_PATH = "api/assets/audio_sample.mp3"
	try:
		import time
		time.sleep(4)
		if not os.path.exists(DUMMY_AUDIO_PATH):
			return JSONResponse(content={"error": "No saved audio found"}, status_code=404)
		audio = open(DUMMY_AUDIO_PATH, 'rb')
		return StreamingResponse(audio, media_type="audio/mpeg")
	except Exception as e:
		print(f" 💥 Error in /api/get-audio-dummy e {e}")
		return JSONResponse(content={"error":"Internal server error"}, status_code=500)


@router.post("/api/test-speech-analysis")
async def speech_analysis(file: UploadFile = File(...)):
    try:
        video_data = await file.read()
        if(video_data):
          logger.info("Read Video Success")
        transcription = process_video_bytes(video_data)
        logger.info(transcription)
        sentiment_result = analyze_sentiment(transcription)
        return {"transcription": transcription, "sentiment": sentiment_result.dict()}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
      