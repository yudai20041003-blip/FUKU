"""
コーディネート履歴管理モジュール
過去のコーディネートを保存・管理
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class OutfitHistoryManager:
    def __init__(self, data_file: str = "data/outfit_history.json"):
        """
        コーディネート履歴マネージャーの初期化
        
        Args:
            data_file: 履歴データファイルのパス
        """
        self.data_file = data_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """
        履歴データをファイルから読み込む
        
        Returns:
            履歴データのリスト
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"履歴データの読み込みに失敗: {e}")
        
        return []
    
    def _save_history(self) -> bool:
        """
        履歴データをファイルに保存
        
        Returns:
            保存成功時True、失敗時False
        """
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"履歴データの保存に失敗: {e}")
            return False
    
    def add_outfit(self, outfit: Dict, weather: Dict, 
                   destination: str, style: str, rating: int = 0) -> bool:
        """
        コーディネートを履歴に追加
        
        Args:
            outfit: コーディネート情報
            weather: 天気情報
            destination: 行き先
            style: スタイル
            rating: 評価（0-5）
        
        Returns:
            追加成功時True
        """
        history_entry = {
            'id': len(self.history) + 1,
            'date': datetime.now().isoformat(),
            'outfit': outfit,
            'weather': {
                'temperature': weather.get('temperature'),
                'description': weather.get('description'),
                'humidity': weather.get('humidity')
            },
            'destination': destination,
            'style': style,
            'rating': rating,
            'notes': ''
        }
        
        self.history.append(history_entry)
        return self._save_history()
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        履歴を取得（新しい順）
        
        Args:
            limit: 取得する件数の上限
        
        Returns:
            履歴のリスト
        """
        sorted_history = sorted(
            self.history, 
            key=lambda x: x['date'], 
            reverse=True
        )
        
        if limit:
            return sorted_history[:limit]
        return sorted_history
    
    def update_rating(self, outfit_id: int, rating: int) -> bool:
        """
        コーディネートの評価を更新
        
        Args:
            outfit_id: コーディネートID
            rating: 新しい評価（0-5）
        
        Returns:
            更新成功時True
        """
        for entry in self.history:
            if entry['id'] == outfit_id:
                entry['rating'] = rating
                return self._save_history()
        return False
    
    def update_notes(self, outfit_id: int, notes: str) -> bool:
        """
        コーディネートのノートを更新
        
        Args:
            outfit_id: コーディネートID
            notes: メモ内容
        
        Returns:
            更新成功時True
        """
        for entry in self.history:
            if entry['id'] == outfit_id:
                entry['notes'] = notes
                return self._save_history()
        return False
    
    def delete_outfit(self, outfit_id: int) -> bool:
        """
        履歴からコーディネートを削除
        
        Args:
            outfit_id: コーディネートID
        
        Returns:
            削除成功時True
        """
        self.history = [
            entry for entry in self.history 
            if entry['id'] != outfit_id
        ]
        return self._save_history()
    
    def get_statistics(self) -> Dict:
        """
        履歴の統計情報を取得
        
        Returns:
            統計情報の辞書
        """
        if not self.history:
            return {
                'total_outfits': 0,
                'most_used_style': None,
                'most_common_destination': None,
                'average_rating': 0
            }
        
        # スタイルの集計
        style_count = {}
        for entry in self.history:
            style = entry['style']
            style_count[style] = style_count.get(style, 0) + 1
        most_used_style = max(style_count, key=style_count.get) if style_count else None
        
        # 行き先の集計
        dest_count = {}
        for entry in self.history:
            dest = entry['destination']
            dest_count[dest] = dest_count.get(dest, 0) + 1
        most_common_dest = max(dest_count, key=dest_count.get) if dest_count else None
        
        # 平均評価
        rated_entries = [e for e in self.history if e.get('rating', 0) > 0]
        avg_rating = sum(e['rating'] for e in rated_entries) / len(rated_entries) if rated_entries else 0
        
        return {
            'total_outfits': len(self.history),
            'most_used_style': most_used_style,
            'most_common_destination': most_common_dest,
            'average_rating': round(avg_rating, 1),
            'style_distribution': style_count,
            'destination_distribution': dest_count
        }
    
    def search_by_weather(self, temperature_range: tuple) -> List[Dict]:
        """
        天気条件で履歴を検索
        
        Args:
            temperature_range: 温度範囲 (最低, 最高)
        
        Returns:
            マッチした履歴のリスト
        """
        min_temp, max_temp = temperature_range
        results = []
        
        for entry in self.history:
            temp = entry['weather'].get('temperature')
            if temp and min_temp <= temp <= max_temp:
                results.append(entry)
        
        return sorted(results, key=lambda x: x['date'], reverse=True)
    
    def get_favorite_outfits(self, min_rating: int = 4) -> List[Dict]:
        """
        高評価のコーディネートを取得
        
        Args:
            min_rating: 最低評価
        
        Returns:
            高評価コーディネートのリスト
        """
        favorites = [
            entry for entry in self.history 
            if entry.get('rating', 0) >= min_rating
        ]
        
        return sorted(favorites, key=lambda x: x['rating'], reverse=True)
