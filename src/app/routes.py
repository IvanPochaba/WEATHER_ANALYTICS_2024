"""PRESENTATION LAYER - HTTP routy"""
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from .services import WeatherService
from .repository import WeatherRepository

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 1. Dependency injection - Správny spôsob inicializácie vrstiev
def get_service():
    repo = WeatherRepository()
    return WeatherService(repo)


@router.get("/")
async def dashboard(
        request: Request,
        service: WeatherService = Depends(get_service)
):
    try:
        data = await service.compare_cities()

        # POUŽIJEME POMENOVANÉ ARGUMENTY - toto je najbezpečnejšia cesta
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"data": data, "error": None}
        )

    except Exception as e:
        print(f"Log: Nastala chyba: {e}")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"data": {}, "error": str(e)}
        )


@router.get("/api/weather")
async def api_weather(service: WeatherService = Depends(get_service)):
    """JSON API endpoint"""
    return await service.compare_cities()