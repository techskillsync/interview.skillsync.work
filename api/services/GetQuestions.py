from typing import List, Tuple
from io import BytesIO
from utils.GetAudio import get_audio

def get_resume(uuid:str) -> None:
	return None

def get_questions_from_resume(resume:None) -> List[str]:
	return [
			"Hi im Rachel, your interviewer! We will start with an introduction, then I will ask a little about what you’ve been up to, then a question about how you collaborate with teammates, and finally a technical question",
			"Tell me about the microservice you deployed at SkillSync. From what I understand microservices are meant to handle one specific task, hiding the complexity with a simple REST API. Is that correct? If so how did you ensure your microservice was simple to use while performing complicated tasks under the hood?",
			"At UBC Agrobot what did you do when your vision for the website differed from a teammate?",
			"I see on your resume you made a Chess Engine, tell me about an improvement you made to it. How did you identify the area that needed improvement. How did you measure your success in improving the project?",
	]

def get_question_audio_tuples(questions:list[str]) -> List[Tuple[str, BytesIO]]:
	tuples:List[Tuple[str, BytesIO]] = []
	for q in questions:
		tuples.append((q, get_audio(q)))
	return tuples

def get_questions(uuid:str) -> List[Tuple[str, BytesIO]]:
	"""
	Returns an array of tuples, where each tuple is question and its corresponding
	BytesIO audio data.
	"""
	resume = get_resume(uuid)
	questions = get_questions_from_resume(resume)
	tuples = get_question_audio_tuples(questions)
	return tuples