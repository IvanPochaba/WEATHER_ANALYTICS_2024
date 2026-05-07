import pandas as pd
import numpy as np
from pathlib import Path
from fastapi import HTTPException


class WeatherService:
    def __init__(self, repo):
        self.repo = repo

    def _process_weather_data(self, raw_data: dict, city_name: str) -> list:
        """Výpočet metrik a export CSV"""
        df = pd.DataFrame(raw_data['daily'])

        # Business výpočty
        df['s_rel'] = (df['sunshine_duration'] / df['daylight_duration'] * 100).fillna(0)
        df['gdd'] = (df['temperature_2m_mean'] - 5).clip(lower=0)
        df['rdi'] = df.apply(
            lambda row: row['precipitation_sum'] / row['precipitation_hours']
            if row['precipitation_hours'] > 0 else 0, axis=1
        )
        df['di'] = df['wind_speed_10m_max'] * (df['sunshine_duration'] / 3600)

        # Export CSV
        Path("output").mkdir(exist_ok=True)
        df.to_csv(f"output/{city_name.lower()}.csv", index=False)

        # Převedení pro JSON
        return df.rename(columns={'time': 'date'}).to_dict('records')

    async def compare_cities(self) -> dict:
        """Porovnání Bratislav vs Victoria"""
        cities = {
            "Bratislava": (48.1486, 17.1077),
            "Victoria": (48.4284, -123.3656)
        }

        result = {}
        for city, (lat, lon) in cities.items():
            data = await self.repo.get_historical_data(lat, lon, "2024-03-02", "2024-03-15")
            result[city] = self._process_weather_data(data, city)

        return result
