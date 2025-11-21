"""
天気情報サービスのテスト
"""
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weather import WeatherService


def test_weather_service_initialization():
    """天気サービスの初期化テスト"""
    service = WeatherService()
    assert service is not None
    assert service.base_url == "https://api.openweathermap.org/data/2.5/weather"


def test_dummy_weather_data():
    """ダミー天気データのテスト"""
    service = WeatherService()
    weather = service._get_dummy_weather()
    
    assert isinstance(weather, dict)
    assert 'temperature' in weather
    assert 'humidity' in weather
    assert 'wind_speed' in weather
    assert 'description' in weather
    assert 'city' in weather


def test_get_weather_without_api_key():
    """APIキーなしでの天気取得テスト（ダミーデータ）"""
    service = WeatherService(api_key='your_api_key_here')
    weather = service.get_weather('Tokyo')
    
    assert weather is not None
    assert isinstance(weather, dict)
    assert 'temperature' in weather


def test_clothing_recommendation():
    """服装推奨のテスト"""
    service = WeatherService()
    
    # 寒い天気
    cold_weather = {
        'temperature': 5,
        'humidity': 60,
        'wind_speed': 3,
        'main': 'Clear'
    }
    rec = service.get_clothing_recommendation(cold_weather)
    assert 'outer' in rec
    assert 'top' in rec
    assert 'bottom' in rec
    assert 'accessories' in rec
    assert any('コート' in item for item in rec['outer'])
    
    # 暑い天気
    hot_weather = {
        'temperature': 30,
        'humidity': 70,
        'wind_speed': 2,
        'main': 'Clear'
    }
    rec = service.get_clothing_recommendation(hot_weather)
    assert 'Tシャツ' in str(rec['top'])
    
    # 雨の天気
    rainy_weather = {
        'temperature': 20,
        'humidity': 80,
        'wind_speed': 5,
        'main': 'Rain'
    }
    rec = service.get_clothing_recommendation(rainy_weather)
    assert '傘' in rec['accessories']
    assert len(rec['notes']) > 0


def test_temperature_ranges():
    """温度範囲ごとの推奨テスト"""
    service = WeatherService()
    
    temperatures = [0, 5, 10, 15, 20, 25, 30]
    
    for temp in temperatures:
        weather = {
            'temperature': temp,
            'humidity': 50,
            'wind_speed': 2,
            'main': 'Clear'
        }
        rec = service.get_clothing_recommendation(weather)
        
        assert isinstance(rec, dict)
        assert 'outer' in rec
        assert 'top' in rec
        assert 'bottom' in rec


if __name__ == '__main__':
    print("Running weather service tests...")
    
    test_weather_service_initialization()
    print("✓ Initialization test passed")
    
    test_dummy_weather_data()
    print("✓ Dummy weather data test passed")
    
    test_get_weather_without_api_key()
    print("✓ Get weather without API key test passed")
    
    test_clothing_recommendation()
    print("✓ Clothing recommendation test passed")
    
    test_temperature_ranges()
    print("✓ Temperature ranges test passed")
    
    print("\nAll tests passed! ✅")
