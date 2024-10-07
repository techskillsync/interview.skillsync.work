'''
Converts Video to Text from video buffer
Call process_video_bytes and pass video buffer in arg
'''

import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import ffmpeg
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


wav2vec_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(device)
wav2vec_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")


def pad_audio(input_values, min_length=16000):
    if input_values.shape[-1] < min_length:
        pad_size = min_length - input_values.shape[-1]
        input_values = torch.nn.functional.pad(input_values, (0, pad_size))
    return input_values


def prepare_audio(waveform, sample_rate, target_rate=16000, min_length=16000):
    if sample_rate != target_rate:
        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=target_rate
        )
        waveform = resampler(waveform)
    logger.info(
        f"Original waveform shape: {waveform.shape}, sample rate: {sample_rate}"
    )
    if waveform.shape[0] > 1:
        logger.info("Converting stereo to mono")
        waveform = torch.mean(waveform, dim=0).unsqueeze(0)
    waveform = pad_audio(waveform.squeeze(), min_length)
    return waveform


def transcribe_audio(waveform, sample_rate):
    audio_input = prepare_audio(waveform, sample_rate, target_rate=16000)
    audio_input = audio_input.to(device)
    audio_input = audio_input.numpy()
    inputs = wav2vec_processor(
        audio_input, sampling_rate=16000, return_tensors="pt", padding="longest"
    ).input_values.to(device)
    logits = wav2vec_model(inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = wav2vec_processor.batch_decode(predicted_ids)[0]
    if not transcription:
        raise ValueError("Failed to transcribe audio")
    return transcription


def video_to_audio_in_memory(video_data: bytes):
    audio_buffer = BytesIO()
    try:
        process = (
            ffmpeg.input("pipe:", format="mp4")
            .output("pipe:", format="wav")
            .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        )
        stdout, stderr = process.communicate(input=video_data)
        if stderr:
            logger.error(f"FFmpeg stderr: {stderr.decode()}")
        audio_buffer.write(stdout)
        audio_buffer.seek(0)       
        audio_data_length = len(stdout)
        logger.info(f"Extracted audio data length: {audio_data_length} bytes")      
        if audio_data_length == 0:
            raise ValueError("No audio data extracted from the video.")
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e.stderr.decode()}")
        raise
    return audio_buffer


def process_video_bytes(video_data: bytes):
    """
    Processes a video file provided as bytes and extracts the transcribed text from its audio.

    This function converts the video file into an audio waveform using FFmpeg, prepares the audio
    by resampling and converting it to mono if necessary, and then transcribes the speech in the
    audio using a Wav2Vec2 model.

    Args:
        video_data (bytes): The input video data in bytes format (e.g., MP4 file).

    Returns:
        str: The transcribed text extracted from the video's audio.

    Raises:
        ValueError: If no audio is extracted from the video, or if the audio contains no data.
        ffmpeg.Error: If there is an error during audio extraction via FFmpeg.

    Example:
        with open("example.mp4", "rb") as f:
            video_bytes = f.read()
        transcription = process_video_bytes(video_bytes)
        print(transcription)  # Output: "Transcribed speech from the video's audio"
    """
    logger.info(device)
    audio_buffer = video_to_audio_in_memory(video_data)
    logger.info("check!!!")
    if len(audio_buffer.getvalue()) == 0:
        raise ValueError("Empty audio buffer")
    waveform, sample_rate = torchaudio.load(audio_buffer, format="wav")
    if waveform.numel() == 0:
        raise ValueError("Loaded audio contains no data")
    print("Waveform shape:", waveform.shape)
    print("Sample rate:", sample_rate)
    transcription = transcribe_audio(waveform, sample_rate)
    return transcription
