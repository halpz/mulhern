from google.cloud import texttospeech
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from io import BytesIO
from pydantic import BaseModel

router = APIRouter()
client = texttospeech.TextToSpeechClient()

class SpeakRequest(BaseModel):
    text: str

@router.post("/speak")
async def synthesize_speech(request: SpeakRequest):
    synthesis_input = texttospeech.SynthesisInput({"text": request.text})

    voice = texttospeech.VoiceSelectionParams(
        {"language_code": "en-GB", "ssml_gender": texttospeech.SsmlVoiceGender.MALE}
    )

    audio_config = texttospeech.AudioConfig(
        {"audio_encoding": texttospeech.AudioEncoding.MP3}
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audio_stream = BytesIO(response.audio_content)

    return StreamingResponse(audio_stream, media_type="audio/mp3", headers={
        "Content-Disposition": "attachment; filename=output.mp3"
    })