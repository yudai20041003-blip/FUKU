"""
AI画像分析モジュール
服の画像を分析してアイテム情報を自動認識
"""
import base64
from typing import Dict, List, Optional
import json


class AIClothingAnalyzer:
    def __init__(self):
        """AI画像分析システムの初期化"""
        self.category_keywords = {
            'outer': ['ジャケット', 'コート', 'アウター', 'ブルゾン', 'パーカー', 'カーディガン'],
            'top': ['Tシャツ', 'シャツ', 'トップス', 'セーター', 'ニット', 'ポロシャツ'],
            'bottom': ['パンツ', 'ズボン', 'ジーンズ', 'デニム', 'スラックス', 'ショーツ'],
            'shoes': ['靴', 'スニーカー', 'ブーツ', 'ローファー', 'サンダル', 'シューズ'],
            'accessories': ['帽子', 'キャップ', 'バッグ', 'ベルト', 'ネクタイ', '時計']
        }
    
    def analyze_clothing_image(self, image_data: bytes) -> Dict:
        """
        服の画像を分析してアイテム情報を抽出
        
        Args:
            image_data: 画像データ（バイナリ）
        
        Returns:
            分析結果（アイテム名、色、カテゴリー、スタイル、説明など）
        """
        # Base64エンコード
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 画像分析用のプロンプト
        analysis_prompt = """
この服の画像を詳しく分析してください。以下の情報をJSON形式で返してください：

{
    "item_name": "アイテムの名前（例: デニムジャケット、白いTシャツ）",
    "category": "カテゴリー（outer/top/bottom/shoes/accessories）",
    "color": "主な色（例: ブルー、ブラック、ホワイト）",
    "style": "スタイル（カジュアル/ストリート/シティ/フォーマル/アメカジ/モード/ベーシック）",
    "material": "素材（例: デニム、コットン、ウール）",
    "pattern": "柄（例: 無地、ストライプ、チェック）",
    "season": ["適した季節（春、夏、秋、冬）"],
    "description": "アイテムの詳細な説明",
    "versatility_score": "汎用性スコア（1-10、高いほど様々なコーデに使える）",
    "recommended_combinations": ["このアイテムと合わせやすいアイテム3-5個"]
}

できるだけ正確に、日本のファッション用語を使って回答してください。
"""
        
        # ここでは、understand_images関数を使って画像を分析します
        # 実際の実装はapp.pyで行います
        return {
            "prompt": analysis_prompt,
            "image_base64": f"data:image/jpeg;base64,{image_base64}"
        }
    
    def analyze_wardrobe_gap(self, wardrobe: Dict, preferred_styles: List[str]) -> Dict:
        """
        ワードローブの穴を分析し、買い足すべきアイテムを提案
        
        Args:
            wardrobe: 現在のワードローブ
            preferred_styles: 好みのスタイル
        
        Returns:
            提案アイテムリストと理由
        """
        gaps = {
            'missing_basics': [],
            'versatile_additions': [],
            'style_enhancers': [],
            'seasonal_needs': []
        }
        
        # 基本アイテムのチェック
        basic_items = {
            'outer': ['デニムジャケット', '黒いジャケット'],
            'top': ['白Tシャツ', 'シャツ', 'ニット'],
            'bottom': ['デニムパンツ', '黒いパンツ'],
            'shoes': ['白スニーカー', '革靴'],
        }
        
        for category, basics in basic_items.items():
            existing_items = [item.get('name', '').lower() for item in wardrobe.get(category, [])]
            for basic in basics:
                if not any(basic.lower() in existing for existing in existing_items):
                    gaps['missing_basics'].append({
                        'category': category,
                        'item': basic,
                        'reason': f'{basic}は汎用性が高く、様々なコーディネートに使えます'
                    })
        
        return gaps
    
    def suggest_outfit_from_images(self, wardrobe: Dict, weather_data: Dict, 
                                   destination: str, preferred_style: str) -> Dict:
        """
        ワードローブの画像から最適なコーディネートを提案
        
        Args:
            wardrobe: ワードローブデータ
            weather_data: 天気情報
            destination: 行き先
            preferred_style: 好みのスタイル
        
        Returns:
            コーディネート提案
        """
        suggestion = {
            'outfit': {},
            'reasoning': [],
            'missing_items': [],
            'alternative_items': []
        }
        
        temp = weather_data.get('temperature', 20)
        
        # 天気に基づいてアイテムを選択
        # アウター
        if temp < 10:
            suggestion['reasoning'].append(f"🌡️ 気温{temp}°Cと寒いので、厚手のアウターが必要です")
        elif temp < 20:
            suggestion['reasoning'].append(f"🌡️ 気温{temp}°Cで少し肌寒いので、軽めのアウターがおすすめです")
        else:
            suggestion['reasoning'].append(f"🌡️ 気温{temp}°Cと暖かいので、アウターは不要です")
        
        return suggestion
    
    def calculate_versatility_score(self, item: Dict, wardrobe: Dict) -> Dict:
        """
        アイテムの汎用性スコアを計算
        
        Args:
            item: アイテム情報
            wardrobe: 現在のワードローブ
        
        Returns:
            汎用性スコアと詳細
        """
        score = 5  # 基本スコア
        details = []
        
        # 色による評価
        color = item.get('color', '').lower()
        neutral_colors = ['黒', 'ブラック', '白', 'ホワイト', 'グレー', 'ネイビー', '紺', 'ベージュ']
        if any(nc in color for nc in neutral_colors):
            score += 2
            details.append('✅ ベーシックカラーで合わせやすい')
        
        # スタイルによる評価
        style = item.get('style', '').lower()
        if 'ベーシック' in style or 'カジュアル' in style:
            score += 1
            details.append('✅ 汎用性の高いスタイル')
        
        # パターンによる評価
        pattern = item.get('pattern', '').lower()
        if '無地' in pattern:
            score += 1
            details.append('✅ 無地で組み合わせやすい')
        
        # 季節による評価
        seasons = item.get('season', '').split(',')
        if len(seasons) >= 3:
            score += 1
            details.append('✅ 3シーズン以上使える')
        
        return {
            'score': min(score, 10),
            'details': details,
            'rating': '高' if score >= 8 else '中' if score >= 6 else '低'
        }
