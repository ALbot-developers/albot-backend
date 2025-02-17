from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.schemas.connection_state import ConnectionStateCreate
from app.services import connection_state

router = APIRouter()


@router.post("/{guild_id}/connection_states")
async def create_connection_states_api(
        guild_id: int,
        options: ConnectionStateCreate,
        _auth=Security(verify_bearer_token)
):
    # connection_statesデータを作成
    connection_states = await connection_state.create(guild_id, options)
    return {
        "message": "Updated guild data.",
        "data": {
            "connection_states": connection_states
        }
    }
