import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.weather_service import WeatherService

@pytest.fixture
def weather_service():
    return WeatherService()

@pytest.mark.asyncio
async def test_analyze_weather_suitability(weather_service):
    # Mock weather data
    weather_data = {
        "main": {"temp": 25},
        "wind": {"speed": 5},
        "weather": [{"main": "Clear"}],
        "rain": {},
        "snow": {}
    }
    
    result = weather_service.analyze_weather_suitability(weather_data, "outdoor")
    
    assert result["suitability"] == "Good"
    assert result["score"] >= 80
    assert isinstance(result["reasons"], list)

def test_analyze_weather_with_error(weather_service):
    weather_data = {"error": "API Error"}
    
    result = weather_service.analyze_weather_suitability(weather_data, "outdoor")
    
    assert result["suitability"] == "Unknown"
    assert result["score"] == 0
    assert "Weather data unavailable" in result["reasons"]

@pytest.mark.asyncio
async def test_get_current_weather_success(weather_service):
    # Mock the HTTP response directly
    mock_response_data = {"main": {"temp": 20}}
    
    with patch('httpx.AsyncClient') as mock_client:
        # Create a proper async context manager mock
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        
        # Mock the response
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_response.raise_for_status = MagicMock()
        
        # Mock the get method to return the response
        mock_instance.get = AsyncMock(return_value=mock_response)
        
        result = await weather_service.get_current_weather("London")
        
        assert "main" in result
        assert result["main"]["temp"] == 20

@pytest.mark.asyncio 
async def test_get_current_weather_error(weather_service):
    # Test error handling with proper async mocking
    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        
        # Mock the get method to raise an exception
        mock_instance.get = AsyncMock(side_effect=Exception("API Error"))
        
        result = await weather_service.get_current_weather("InvalidCity")
        
        assert "error" in result
        assert result["error"] == "Failed to fetch weather data"
