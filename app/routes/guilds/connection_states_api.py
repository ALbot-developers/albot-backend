from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.schemas.api_data import ConnectionStateData
from app.schemas.api_response import ConnectionStateAPIResponse
from app.schemas.connection_state import ConnectionStateCreate
from app.services import connection_state

router = APIRouter()


@router.post("/{guild_id}/connection_states", response_model=ConnectionStateAPIResponse)
async def create_connection_states_api(
        guild_id: int,
        options: ConnectionStateCreate,
        _auth=Security(verify_bearer_token)
):
    return ConnectionStateAPIResponse(
        message="Created connection states.",
        data=ConnectionStateData(
            connection_states=await connection_state.create(guild_id, options)
        )
    )
