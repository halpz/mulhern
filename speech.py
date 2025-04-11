import base64
import os

import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from io import BytesIO
from pydantic import BaseModel

router = APIRouter()

GOOGLE_TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

AUTH_TOKEN = os.environ.get("TTS_KEY")
if not AUTH_TOKEN:
    with open("speechKey.txt") as f:
        AUTH_TOKEN = f.read().strip()

class SpeakRequest(BaseModel):
    text: str

@router.post("/speak")
async def synthesize_speech(request: SpeakRequest):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-User-Project": "gov-sound",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    payload = {
        "input": {
            "text": request.text
        },
        "voice": {
            "languageCode": "en-GB",
            "name": "en-GB-Chirp3-HD-Puck"
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TTS_URL, headers=headers, json=payload)

    response.raise_for_status()
    data = response.json()

    audio_content = base64.b64decode(data["audioContent"])
    audio_stream = BytesIO(audio_content)

    return StreamingResponse(audio_stream, media_type="audio/wav", headers={
        "Content-Disposition": "attachment; filename=output.wav"
    })
