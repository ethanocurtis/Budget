from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from ...utils.deps import get_db, get_current_user
from ...core.config import settings
import os

router = APIRouter()

@router.get("/attachments/{filename}")
def get_attachment(filename: str, user=Depends(get_current_user)):
    path = os.path.join(settings.media_root, filename)
    if not os.path.exists(path):
        return {"error": "not found"}
    return FileResponse(path)
