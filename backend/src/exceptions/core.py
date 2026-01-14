from pathlib import Path

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from backend.src.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/templates/")


def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/error.html",
        {"request": request,
         "status_code": exc.status_code,
         "detail": exc.detail,
         "site_name": settings.SITENAME,
         "current_year": settings.current_year,
         "header_image": settings.HEADER_IMAGE,}
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        "errors/error.html",
        {"request": request,
         "status_code": 422,
         "detail": exc.errors()[0]["msg"],
         "site_name": settings.SITENAME,
         "current_year": settings.current_year,
         "header_image": settings.HEADER_IMAGE,}
    )