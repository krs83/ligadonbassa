from pathlib import Path

from fastapi import Request, Query
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.src.dependencies import athlete_serviceDP
from backend.src.exceptions.athlete import AthleteNotFoundException

router = APIRouter(include_in_schema=False, prefix="/athletes")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/templates/")


@router.get("/", response_class=HTMLResponse)
async def get_all_athletes_html(
        request: Request,
        athlete_service: athlete_serviceDP,
        offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
        limit: int = Query(default=50, le=500, description="Лимит записей на страницу"),
        search: str = Query(default=None, description="Поиск спортсмена по имени"),

):
    if search:
        athletes = await athlete_service.search_athlete_byname(search)
    else:
        athletes = await athlete_service.get_athletes(offset, limit)


    # Проверяем HTMX запрос
    if request.headers.get("hx-request"):
        template = "athletes/athletes_fragment.html"
    else:
        template = "athletes/athletes.html"

    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "athletes": athletes,
            "offset": offset,
            "limit": limit,
            "search_query": search or "",
        }
    )


@router.get("/{athlete_id}", response_class=HTMLResponse)
async def get_athlete_detail(
        request: Request,
        athlete_id: int,
        athlete_service: athlete_serviceDP,
):
    try:
        athlete = await athlete_service.get_athlete(athlete_id)
    except AthleteNotFoundException:
        # Если атлет не найден, возвращаем на список атлетов
        return templates.TemplateResponse(
            "athletes/athletes.html",
            {
                "request": request,
                "athletes": [],
                "error": f"Атлет с ID {athlete_id} не найден"
            }
        )

    # Проверяем HTMX запрос
    if request.headers.get("hx-request"):
        template = "athletes/athlete_detail_fragment.html"
    else:
        template = "athletes/athlete_detail.html"

    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "athlete": athlete
        }
    )