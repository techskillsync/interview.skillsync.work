"""
Call GetAudio to turn some text into an audio BytesIO object
"""

import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from io import BytesIO

client = ElevenLabs(api_key=os.getenv('ELEVEN_LABS_API_KEY'))


def GetAudio(question: str) -> BytesIO:
	"""
	Returns the string read aloud
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
	pass
