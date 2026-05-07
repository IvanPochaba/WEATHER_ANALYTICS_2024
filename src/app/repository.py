import httpx
from fastapi import HTTPException, status
from typing import Dict

class WeatherRepository:
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    async def get_historical_data(self, lat: float, lon: float, start: str, end: str) -> Dict:
        """Získání historických dat z Open-Meteo"""
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start,
            "end_date": end,
            "daily": [
                "temperature_2m_mean",
                "wind_speed_10m_max",
                "precipitation_sum",
                "precipitation_hours",
                "sunshine_duration",
                "daylight_duration"
            ],
            "timezone": "GMT"
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()

                if response.status_code >= 400:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"API chyba: {response.status_code}"
                    )

                return response.json()

            except httpx.ConnectError:
                raise HTTPException(503, "Server nedostupný")
            except Exception as e:
                raise HTTPException(500, f"Chyba: {str(e)}")
