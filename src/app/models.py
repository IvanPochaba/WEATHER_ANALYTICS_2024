from pydantic import BaseModel  # Importuje základnú triedu pre tvorbu dátových schém
from typing import List, Dict  # Importuje typy pre zoznamy a slovníky na typovú anotáciu
from typing import ClassVar

class DailyMetric(BaseModel):  # Definuje schému pre denné meteorologické metriky
    date: str                  # Dátum merania ako reťazec
    s_rel: float               # Relatívny slnečný svit (výpočet v service)
    gdd: float                 # Growing Degree Days (vyjadruje rastový potenciál rastlín pre danú teplotu)
    rdi: float                 # Index intenzity dažďa
    di: float

class WeatherResponse(BaseModel):
    cities: ClassVar[dict] = {
        "Bratislava": List[DailyMetric],
        "Victoria": List[DailyMetric]
    }