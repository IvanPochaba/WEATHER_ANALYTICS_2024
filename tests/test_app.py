import pytest
from unittest.mock import AsyncMock, patch
from src.app.services import WeatherService


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.get_historical_data.return_value = {
        "daily": {"time": ["2024-03-02"], "temperature_2m_mean": [10]}
    }
    return repo


@pytest.mark.asyncio
async def test_compare_cities(mock_repo):
    service = WeatherService(mock_repo)
    result = await service.compare_cities()

    assert "Bratislava" in result
    assert len(result["Bratislava"]) == 1