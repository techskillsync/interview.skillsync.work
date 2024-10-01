from typing import Iterator
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from io import BytesIO

client = ElevenLabs(api_key="sk_acfadd44aa7740ac1a954674e3080cc34d367b6f1e8d623e")


def GetAudio(question: str) -> BytesIO:
	"""
	Returns a tuple (question_text, audio_bytes)
	"""
	audio_iterator = client.generate(
		text=question, voice="Callum", model="eleven_multilingual_v2"
	)
	
	audio_bytes = BytesIO()
	for chunk in audio_iterator:
		audio_bytes.write(chunk)

	audio_bytes.seek(0)

	return audio_bytes


if __name__ == "__main__":
	# GetQuestion()
	pass
