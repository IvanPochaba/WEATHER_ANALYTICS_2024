"""🚀 FASTAPI APLIKACE - Community Edition"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.routes import router
from app import WeatherService, WeatherRepository

app = FastAPI(
    title="🌤️ Weather Analytics 2024",
    description="Bratislava vs Victoria | 3-vrstvová architektura",
    version="1.0.0-community"
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Weather Analytics API", "docs": "/docs", "dashboard": "/"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)