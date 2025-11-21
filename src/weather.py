"""
天気情報取得モジュール
OpenWeatherMap APIを使用して現在の天気情報を取得
"""
import requests
import os
from typing import Dict, Optional


class WeatherService:
    def __init__(self, api_key: Optional[str] = None):
        """
        天気情報サービスの初期化
        
        Args:
            api_key: OpenWeatherMap APIキー
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def _translate_city_name(self, city: str) -> str:
        """
        日本語の都市名を英語に変換
        
        Args:
            city: 都市名（日本語または英語）
        
        Returns:
            英語の都市名
        """
        try:
            from japan_cities import translate_city_to_english
            return translate_city_to_english(city)
        except ImportError:
            # フォールバック: 基本的な変換テーブル
            city_translations = {
                '東京': 'Tokyo',
                '大阪': 'Osaka',
                '名古屋': 'Nagoya',
                '札幌': 'Sapporo',
                '福岡': 'Fukuoka',
                '京都': 'Kyoto',
                '横浜': 'Yokohama',
                '神戸': 'Kobe',
                '仙台': 'Sendai',
                '広島': 'Hiroshima'
            }
            return city_translations.get(city, city)
    
    def get_weather(self, city: str = "Tokyo", country: str = "") -> Optional[Dict]:
        """
        指定された都市の天気情報を取得
        
        Args:
            city: 都市名（日本語または英語）
            country: 国コード（JP, US等、空文字の場合は自動判定）
        
        Returns:
            天気情報の辞書、エラーの場合はNone
        """
        if not self.api_key or self.api_key == 'your_api_key_here':
            # APIキーがない場合はダミーデータを返す
            return self._get_dummy_weather(city)
        
        # 日本語の都市名を英語に変換
        translated_city = self._translate_city_name(city)
        
        try:
            # 国コードが指定されていない場合は都市名のみで検索
            if country:
                query = f"{translated_city},{country}"
            else:
                query = translated_city
            
            params = {
                'q': query,
                'appid': self.api_key,
                'units': 'metric',  # 摂氏温度
                'lang': 'ja'  # 日本語
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'], 1),
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'city': data['name']
            }
        
        except requests.exceptions.RequestException as e:
            print(f"天気情報の取得に失敗しました: {e}")
            return self._get_dummy_weather(translated_city)
    
    def _get_dummy_weather(self, city: str = "Tokyo") -> Dict:
        """
        デモ用のダミー天気データを返す
        
        Args:
            city: 都市名
        
        Returns:
            ダミー天気情報
        """
        return {
            'temperature': 20,
            'feels_like': 18,
            'humidity': 60,
            'wind_speed': 3.5,
            'description': '晴れ',
            'main': 'Clear',
            'city': f'{city} (デモデータ)'
        }
    
    def get_clothing_recommendation(self, weather_data: Dict) -> Dict:
        """
        天気情報に基づいて服装の推奨を取得
        気温、体感温度、湿度、風速を総合的に考慮
        
        Args:
            weather_data: 天気情報の辞書
        
        Returns:
            服装推奨の辞書
        """
        temp = weather_data['temperature']
        feels_like = weather_data['feels_like']
        humidity = weather_data['humidity']
        wind = weather_data['wind_speed']
        
        # 体感温度を優先的に使用
        effective_temp = feels_like if abs(feels_like - temp) > 2 else temp
        
        # より細かい温度段階に基づく推奨（2-3度刻み）
        if effective_temp < 0:
            base = {
                'outer': ['ダウンジャケット', '厚手のウールコート', '中綿コート'],
                'top': ['極厚ニット', 'ヒートテックインナー+セーター', 'フリース'],
                'bottom': ['裏起毛パンツ', 'ウールパンツ', '厚手のデニム'],
                'accessories': ['マフラー', '手袋', 'ニット帽', 'イヤーマフ'],
                'temp_advice': f'非常に寒い気温です（{effective_temp}°C）。完全防寒が必要です。'
            }
        elif effective_temp < 5:
            base = {
                'outer': ['ダウンジャケット', '厚手のコート', 'ウールコート'],
                'top': ['厚手のニット', 'セーター', 'フリース'],
                'bottom': ['厚手のパンツ', 'ウールパンツ', 'デニム'],
                'accessories': ['マフラー', '手袋', 'ニット帽'],
                'temp_advice': f'かなり寒い気温です（{effective_temp}°C）。しっかりとした防寒が必要です。'
            }
        elif effective_temp < 8:
            base = {
                'outer': ['厚手のコート', 'ウールコート', 'ダッフルコート'],
                'top': ['ニット', 'セーター', '厚手の長袖シャツ'],
                'bottom': ['長ズボン', 'ウールパンツ', 'チノパン'],
                'accessories': ['マフラー', 'ストール', '手袋'],
                'temp_advice': f'寒い気温です（{effective_temp}°C）。コートとニットで温かく。'
            }
        elif effective_temp < 12:
            base = {
                'outer': ['コート', 'ジャケット', 'トレンチコート'],
                'top': ['ニット', 'セーター', '長袖シャツ'],
                'bottom': ['長ズボン', 'チノパン', 'ジーンズ'],
                'accessories': ['マフラー', 'ストール'],
                'temp_advice': f'肌寒い気温です（{effective_temp}°C）。アウターは必須です。'
            }
        elif effective_temp < 15:
            base = {
                'outer': ['軽めのジャケット', 'カーディガン', 'スプリングコート'],
                'top': ['長袖シャツ', '薄手のニット', 'ロンT'],
                'bottom': ['長ズボン', 'チノパン', 'ジーンズ'],
                'accessories': ['ストール'],
                'temp_advice': f'少し涼しい気温です（{effective_temp}°C）。軽めのアウターがちょうど良いです。'
            }
        elif effective_temp < 18:
            base = {
                'outer': ['薄手のジャケット', 'カーディガン', 'パーカー'],
                'top': ['長袖シャツ', 'ロンT', '薄手のニット'],
                'bottom': ['長ズボン', 'チノパン', 'デニム'],
                'accessories': [],
                'temp_advice': f'過ごしやすい気温です（{effective_temp}°C）。アウターは持ち歩く程度で。'
            }
        elif effective_temp < 21:
            base = {
                'outer': ['薄手のカーディガン', '軽いジャケット'],
                'top': ['長袖シャツ', 'ロンT', '薄手のカットソー'],
                'bottom': ['長ズボン', 'チノパン'],
                'accessories': [],
                'temp_advice': f'快適な気温です（{effective_temp}°C）。アウターは念のため持参を。'
            }
        elif effective_temp < 24:
            base = {
                'outer': [],
                'top': ['半袖シャツ', 'Tシャツ', 'ポロシャツ', '薄手の長袖'],
                'bottom': ['長ズボン', 'チノパン', '薄手のパンツ'],
                'accessories': ['サングラス'],
                'temp_advice': f'暖かい気温です（{effective_temp}°C）。軽装で快適に過ごせます。'
            }
        elif effective_temp < 27:
            base = {
                'outer': [],
                'top': ['半袖シャツ', 'Tシャツ', 'ポロシャツ'],
                'bottom': ['長ズボン', 'チノパン', 'ショートパンツ'],
                'accessories': ['サングラス', '帽子'],
                'temp_advice': f'暑い気温です（{effective_temp}°C）。涼しい素材を選びましょう。'
            }
        elif effective_temp < 30:
            base = {
                'outer': [],
                'top': ['半袖シャツ', 'Tシャツ', 'タンクトップ', 'リネンシャツ'],
                'bottom': ['ショートパンツ', '薄手のパンツ', 'リネンパンツ'],
                'accessories': ['サングラス', '帽子', 'ハンカチ'],
                'temp_advice': f'かなり暑い気温です（{effective_temp}°C）。通気性の良い服装で。'
            }
        else:
            base = {
                'outer': [],
                'top': ['半袖シャツ', 'Tシャツ', 'タンクトップ'],
                'bottom': ['ショートパンツ', '薄手のパンツ'],
                'accessories': ['サングラス', '帽子', 'ハンカチ', '日傘'],
                'temp_advice': f'非常に暑い気温です（{effective_temp}°C）。熱中症に注意してください。'
            }
        
        # 湿度と風の詳細な調整
        notes = []
        
        # 体感温度の注意喚起
        if abs(feels_like - temp) > 3:
            if feels_like < temp:
                notes.append(f'⚠️ 風で体感温度が{abs(feels_like - temp):.1f}度低く感じます')
            else:
                notes.append(f'⚠️ 湿度で体感温度が{abs(feels_like - temp):.1f}度高く感じます')
        
        # 湿度への対応
        if humidity > 80:
            notes.append('💧 湿度がかなり高いです（{humidity}%）。速乾性・通気性の良い素材がおすすめです')
            if effective_temp > 25:
                notes.append('⚠️ 蒸し暑さに注意。こまめな水分補給を')
        elif humidity > 70:
            notes.append(f'💧 湿度が高めです（{humidity}%）。通気性の良い素材がおすすめです')
        elif humidity < 30:
            notes.append(f'💨 空気が乾燥しています（{humidity}%）。保湿対策をお忘れなく')
        
        # 風への対応
        if wind > 8:
            notes.append(f'🌬️ 強風です（{wind}m/s）。防風性の高いアウターと固定できる帽子がおすすめです')
            if effective_temp < 15:
                notes.append('⚠️ 風により体感温度がかなり下がります')
        elif wind > 5:
            notes.append(f'🌬️ 風が強めです（{wind}m/s）。防風性のあるアウターがおすすめです')
        
        # 天気への対応
        if weather_data['main'] in ['Rain', 'Drizzle']:
            notes.append('☔ 雨が予想されます。防水性のある服装と傘を用意してください')
            base['accessories'].append('傘')
            if 'レインコート' not in base['outer']:
                base['outer'].insert(0, 'レインコート')
        elif weather_data['main'] == 'Thunderstorm':
            notes.append('⛈️ 雷雨の可能性があります。防水対策をしっかりと')
            base['accessories'].append('傘')
        elif weather_data['main'] == 'Snow':
            notes.append('⛄ 雪が予想されます。滑りにくい靴と防寒・防水対策を')
            base['accessories'].append('防水ブーツ')
        
        # 紫外線対策
        if effective_temp > 20 and weather_data['main'] in ['Clear', 'Clouds']:
            notes.append('☀️ 紫外線対策もお忘れなく')
        
        base['notes'] = notes
        base['actual_temp'] = temp
        base['feels_like_temp'] = feels_like
        
        return base
