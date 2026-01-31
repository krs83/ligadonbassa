from pathlib import Path

from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.requests import Request

from backend.src.api.athlete import router as athlete_router
from backend.src.api.user import router as user_router
from backend.src.api.auth import router as auth_router
from backend.src.api.tournament import router as tournament_router
from backend.src.api.athlete_tournament_link import router as athlete_tournament_link_router
from backend.src.exceptions.core import not_found_error, validation_exception_handler

from frontend.endpoints.athletes import router as athlete_html_router
from frontend.endpoints.index import router as index_router

from backend.src.admin.setup import setup_admin
from backend.src.config import settings

app = FastAPI(title=settings.SITENAME, version="1.3.1")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

#global errors handling
@app.exception_handler(404)
async def html_404(request: Request, exc: HTTPException):
    if not "/api/" in request.url.path:
        return not_found_error(request, exc)
    else:
        return JSONResponse(
            status_code=404,
            content={"error": exc.detail}
        )

@app.exception_handler(RequestValidationError)
async def html_422(request: Request, exc: RequestValidationError):
    if not "/api/" in request.url.path:
        return validation_exception_handler(request, exc)
    else:
        return JSONResponse(
            status_code=422,
            content={"error": exc.errors()}
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000", "https://ligadonbassa.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/frontend/static/"), name="static")
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/templates/")


setup_admin(app)

#front routers
app.include_router(athlete_html_router)
app.include_router(index_router)

#back routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(athlete_router, prefix=settings.API_V1_STR)
app.include_router(tournament_router, prefix=settings.API_V1_STR)
app.include_router(athlete_tournament_link_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("backend.src.main:app", host="0.0.0.0", reload=True)
