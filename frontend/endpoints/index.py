from pathlib import Path

from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.src.config import settings
from backend.src.dependencies import athlete_serviceDP

router = APIRouter(include_in_schema=False)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/templates/")


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request,
                    athlete_service: athlete_serviceDP):
    athletes = await athlete_service.get_athletes(offset=0, limit=10)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "site_name": settings.SITENAME,
            "header_image": settings.HEADER_IMAGE,
            "ligadonbassa_image_1": settings.LIGADONBASSA_IMAGE_1,
            "ligadonbassa_image_2": settings.LIGADONBASSA_IMAGE_2,
            "limit": 10,
            "athletes": athletes
        }
    )
