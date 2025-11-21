"""
ワードローブ管理モジュール
ユーザーの持っている服を管理
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class WardrobeManager:
    def __init__(self, data_file: str = "data/wardrobe.json"):
        """
        ワードローブマネージャーの初期化
        
        Args:
            data_file: データファイルのパス
        """
        self.data_file = data_file
        self.wardrobe = self._load_wardrobe()
    
    def _load_wardrobe(self) -> Dict:
        """
        ワードローブデータをファイルから読み込む
        
        Returns:
            ワードローブデータの辞書
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"ワードローブデータの読み込みに失敗: {e}")
        
        # デフォルトのワードローブ構造
        return {
            'outer': [],
            'top': [],
            'bottom': [],
            'shoes': [],
            'accessories': []
        }
    
    def _save_wardrobe(self) -> bool:
        """
        ワードローブデータをファイルに保存
        
        Returns:
            保存成功時True、失敗時False
        """
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.wardrobe, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"ワードローブデータの保存に失敗: {e}")
            return False
    
    def add_item(self, category: str, item: Dict, image_data: Optional[bytes] = None) -> bool:
        """
        ワードローブにアイテムを追加
        
        Args:
            category: カテゴリー（outer, top, bottom, shoes, accessories）
            item: アイテム情報の辞書
            image_data: 画像データ（バイナリ）
        
        Returns:
            追加成功時True、失敗時False
        """
        if category not in self.wardrobe:
            return False
        
        # アイテムにIDとタイムスタンプを追加
        item['id'] = len(self.wardrobe[category]) + 1
        item['added_date'] = datetime.now().isoformat()
        
        # 画像がある場合は保存
        if image_data:
            image_path = self._save_image(category, item['id'], image_data)
            if image_path:
                item['image_path'] = image_path
        
        self.wardrobe[category].append(item)
        return self._save_wardrobe()
    
    def _save_image(self, category: str, item_id: int, image_data: bytes) -> Optional[str]:
        """
        画像データを保存
        
        Args:
            category: カテゴリー
            item_id: アイテムID
            image_data: 画像データ
        
        Returns:
            保存されたパス、失敗時None
        """
        try:
            import base64
            
            # 画像ディレクトリを作成
            img_dir = 'static/images/wardrobe'
            os.makedirs(img_dir, exist_ok=True)
            
            # ファイル名を生成
            filename = f"{category}_{item_id}.png"
            filepath = os.path.join(img_dir, filename)
            
            # 画像を保存
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            return filepath
        except Exception as e:
            print(f"画像の保存に失敗: {e}")
            return None
    
    def remove_item(self, category: str, item_id: int) -> bool:
        """
        ワードローブからアイテムを削除
        
        Args:
            category: カテゴリー
            item_id: アイテムID
        
        Returns:
            削除成功時True、失敗時False
        """
        if category not in self.wardrobe:
            return False
        
        self.wardrobe[category] = [
            item for item in self.wardrobe[category] 
            if item.get('id') != item_id
        ]
        return self._save_wardrobe()
    
    def get_items_by_category(self, category: str) -> List[Dict]:
        """
        カテゴリー別にアイテムを取得
        
        Args:
            category: カテゴリー
        
        Returns:
            アイテムのリスト
        """
        return self.wardrobe.get(category, [])
    
    def get_all_items(self) -> Dict:
        """
        すべてのアイテムを取得
        
        Returns:
            カテゴリー別のアイテム辞書
        """
        return self.wardrobe
    
    def search_items(self, 
                     keywords: Optional[str] = None,
                     color: Optional[str] = None,
                     style: Optional[str] = None,
                     season: Optional[str] = None) -> List[Dict]:
        """
        条件に基づいてアイテムを検索
        
        Args:
            keywords: キーワード
            color: 色
            style: スタイル
            season: 季節
        
        Returns:
            マッチしたアイテムのリスト
        """
        results = []
        
        for category, items in self.wardrobe.items():
            for item in items:
                match = True
                
                if keywords:
                    match = match and any(
                        keywords.lower() in str(v).lower() 
                        for v in item.values()
                    )
                
                if color:
                    match = match and item.get('color', '').lower() == color.lower()
                
                if style:
                    match = match and item.get('style', '').lower() == style.lower()
                
                if season:
                    match = match and season.lower() in item.get('season', '').lower()
                
                if match:
                    results.append({**item, 'category': category})
        
        return results
    
    def get_sample_wardrobe(self) -> Dict:
        """
        サンプルのワードローブデータを取得
        
        Returns:
            サンプルワードローブ
        """
        return {
            'outer': [
                {
                    'id': 1,
                    'name': 'デニムジャケット',
                    'color': 'ブルー',
                    'brand': 'ユニクロ',
                    'style': 'カジュアル',
                    'season': '春,秋'
                },
                {
                    'id': 2,
                    'name': 'レザージャケット',
                    'color': 'ブラック',
                    'brand': 'ZARA',
                    'style': 'ストリート',
                    'season': '秋,冬'
                }
            ],
            'top': [
                {
                    'id': 1,
                    'name': '白シャツ',
                    'color': 'ホワイト',
                    'brand': '無印良品',
                    'style': 'ベーシック',
                    'season': '春,夏,秋,冬'
                },
                {
                    'id': 2,
                    'name': 'オーバーサイズTシャツ',
                    'color': 'ブラック',
                    'brand': 'GU',
                    'style': 'ストリート',
                    'season': '春,夏,秋'
                }
            ],
            'bottom': [
                {
                    'id': 1,
                    'name': 'スキニージーンズ',
                    'color': 'ブラック',
                    'brand': 'ユニクロ',
                    'style': 'カジュアル',
                    'season': '春,秋,冬'
                },
                {
                    'id': 2,
                    'name': 'ワイドパンツ',
                    'color': 'ベージュ',
                    'brand': 'H&M',
                    'style': 'シティ',
                    'season': '春,夏,秋'
                }
            ],
            'shoes': [
                {
                    'id': 1,
                    'name': 'スニーカー',
                    'color': 'ホワイト',
                    'brand': 'Nike',
                    'style': 'カジュアル',
                    'season': '春,夏,秋,冬'
                }
            ],
            'accessories': [
                {
                    'id': 1,
                    'name': 'キャップ',
                    'color': 'ブラック',
                    'brand': 'Supreme',
                    'style': 'ストリート',
                    'season': '春,夏,秋,冬'
                }
            ]
        }
    
    def load_sample_data(self) -> bool:
        """
        サンプルデータをロード
        
        Returns:
            ロード成功時True
        """
        self.wardrobe = self.get_sample_wardrobe()
        return self._save_wardrobe()
