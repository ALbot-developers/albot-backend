from fastapi import APIRouter, Security, UploadFile, File, Form
from starlette.requests import Request

from app.core.auth import verify_all_tokens, verify_session
from app.core.error import CustomHTTPException
from app.external.discord.models import UserPIIResponse
from app.schemas.api_data import ClonedVoice, ClonedVoiceData, ClonedVoicesListData
from app.schemas.api_response import ClonedVoiceAPIResponse, ClonedVoicesListAPIResponse
from app.services.voice_clone import create_voice, save_cloned_voice, list_by_guild

router = APIRouter()

ALLOWED_AUDIO_TYPES = {"audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a", "audio/x-m4a", "audio/mp4"}
MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/{guild_id}/cloned-voices", response_model=ClonedVoiceAPIResponse)
async def create_cloned_voice_api(
        guild_id: int,
        request: Request,
        audio: UploadFile = File(...),
        label: str = Form(...),
        _auth=Security(verify_session)
):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])

    if audio.content_type not in ALLOWED_AUDIO_TYPES:
        raise CustomHTTPException(status_code=400, detail="Unsupported audio format. Supported: WAV, MP3, M4A.")

    audio_data = await audio.read()
    if len(audio_data) > MAX_AUDIO_SIZE:
        raise CustomHTTPException(status_code=400, detail="Audio file too large. Maximum size is 10MB.")

    try:
        voice = await create_voice(audio_data, audio.content_type)
    except RuntimeError as e:
        raise CustomHTTPException(status_code=502, detail=str(e))

    user_id = int(user_info.id)
    await save_cloned_voice(guild_id, user_id, voice, label)

    return ClonedVoiceAPIResponse(
        message="Cloned voice created.",
        data=ClonedVoiceData(voice=ClonedVoice(guild_id=guild_id, user_id=user_id, voice=voice, label=label))
    )


@router.get("/{guild_id}/cloned-voices", response_model=ClonedVoicesListAPIResponse)
async def list_cloned_voices_api(guild_id: int, _auth=Security(verify_all_tokens)):
    rows = await list_by_guild(guild_id)
    voices = [ClonedVoice(**row) for row in rows]
    return ClonedVoicesListAPIResponse(
        message="Fetched cloned voices.",
        data=ClonedVoicesListData(voices=voices)
    )
