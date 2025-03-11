from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.auth.models import User
from src.auth.utils import get_current_user
from src.database import get_db
from src.logs import schemas
from src.logs.client import LogClient

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload", status_code=status.HTTP_200_OK)
def upload_files(
        files: list[UploadFile],
        service: LogClient = Depends(LogClient),
        user: User = Depends(get_current_user)
):
    for file in files:
        service.process_upload(file, user.id)
    return {"description": "Logs uploaded successfully"}


@router.get("/search", response_model=schemas.SearchResponse)
def search_logs(
        params: schemas.SearchParams = Depends(),
        current_user: User = Depends(get_current_user),
):
    log_service = LogClient()

    search_results = log_service.search_user_logs(
        user_id=current_user.id,
        start_time=params.start_time,
        end_time=params.end_time,
        keyword=params.keyword,
        level=params.level
    )

    hits = search_results.get('hits', {})
    return {
        "total": hits.get('total', {}).get('value', 0),
        "logs": [hit['_source'] for hit in hits.get('hits', [])]
    }