import os

from elevenlabs.core import ApiError
from google.cloud import texttospeech
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
from elevenlabs.client import ElevenLabs
import logging


key = os.environ.get("ELEVEN_KEY")
if not key:
    with open("eleven.txt") as f:
        key = f.read().strip()


client = ElevenLabs(
  api_key=key,
)


router = APIRouter()

class SpeakRequest(BaseModel):
    text: str

@router.post("/speak")
async def synthesize_speech(request: SpeakRequest):
    try:
        audio_stream = client.text_to_speech.convert_as_stream(
            text=request.text,
            voice_id="zt0X5NTm9ZAYJ9qvmxSV",
            model_id="eleven_multilingual_v2"
        )
        return StreamingResponse(audio_stream, media_type="audio/mp3", headers={
            "Content-Disposition": "attachment; filename=output.mp3"
        })
    except ApiError as e:
        logging.warning(f"ElevenLabs API error: {e}")
        return await fallback_speech(request)



google_client = texttospeech.TextToSpeechClient()
# @router.post("/speak")
async def fallback_speech(request: SpeakRequest):
    synthesis_input = texttospeech.SynthesisInput({"text": request.text})

    voice = texttospeech.VoiceSelectionParams(
        {"language_code": "en-GB", "ssml_gender": texttospeech.SsmlVoiceGender.MALE}
    )

    audio_config = texttospeech.AudioConfig(
        {"audio_encoding": texttospeech.AudioEncoding.MP3}
    )

    response = google_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audio_stream = BytesIO(response.audio_content)

    return StreamingResponse(audio_stream, media_type="audio/mp3", headers={
        "Content-Disposition": "attachment; filename=output.mp3"
    })