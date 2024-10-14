from services.SpeechAnalysis import analyze_sentiment
from services.Video2Text import process_video_bytes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_speech_from_video(video_data: bytes) -> dict:
    """
    Args:
        video_data (bytes): The video data in bytes format.
    Returns:
        dict: A dictionary containing the transcription and sentiment analysis results.
    Raises:
        Exception: Raises an exception if there is an error during processing.
    """
    try:
        if video_data:
            logger.info("Read Video Success")
        transcription = process_video_bytes(video_data)
        logger.info(f"Transcription: {transcription}")
        sentiment_result = analyze_sentiment(transcription)
        return {
            "transcription": transcription,
            "sentiment": sentiment_result.dict()
        }
    except Exception as e:
        logger.error(f"Error in speech analysis: {str(e)}")
        raise Exception(f"Speech analysis failed: {str(e)}")

def run_speech_analysis(file_path: str) -> None:
    """
    Runs speech analysis on a video file specified by the file path.

    Args:
        file_path (str): The path to the video file.

    Raises:
        Exception: Raises an exception if there is an error during analysis.
    """
    try:
        with open(file_path, "rb") as video_file:
            video_data = video_file.read()
        result = analyze_speech_from_video(video_data)
        print("Transcription:", result["transcription"])
        print("Sentiment:", result["sentiment"])

    except Exception as e:
        print(f"Error during speech analysis: {str(e)}")

#Code runner
if __name__ == "__main__":
    run_speech_analysis("path/to/your/video.mp4")
