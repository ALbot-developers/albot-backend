from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.schemas.guild_dict import DictPut
from app.services import guild_dict

router = APIRouter()


@router.get("/{guild_id}/dict")
async def get_guild_dict_api(guild_id: int, _auth=Security(verify_all_tokens)):
    return {
        "message": "Fetched guild data.",
        "data": {
            "dict": await guild_dict.get(guild_id)
        }
    }


@router.put("/{guild_id}/dict")
async def replace_guild_dict(guild_id: int, data: DictPut, _auth=Security(verify_all_tokens)):
    await guild_dict.update(guild_id, data.dict)
    return {
        "message": "Updated guild data."
    }


@router.delete("/{guild_id}/dict")
async def delete_guild_dict(guild_id: int, _auth=Security(verify_all_tokens)):
    await guild_dict.delete(guild_id)
    return {
        "message": "Deleted guild data."
    }
