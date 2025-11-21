"""
データのエクスポート/インポート機能
ワードローブと履歴データのバックアップと復元
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime
import zipfile
import io


class DataExporter:
    def __init__(self):
        """データエクスポーターの初期化"""
        pass
    
    def export_to_json(self, wardrobe: Dict, history: list) -> str:
        """
        ワードローブと履歴をJSONにエクスポート
        
        Args:
            wardrobe: ワードローブデータ
            history: 履歴データ
        
        Returns:
            JSON文字列
        """
        export_data = {
            'export_date': datetime.now().isoformat(),
            'version': '1.0',
            'wardrobe': wardrobe,
            'history': history
        }
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def export_to_file(self, wardrobe: Dict, history: list, 
                       filename: Optional[str] = None) -> str:
        """
        ワードローブと履歴をファイルにエクスポート
        
        Args:
            wardrobe: ワードローブデータ
            history: 履歴データ
            filename: ファイル名（Noneの場合は自動生成）
        
        Returns:
            保存されたファイルパス
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'fashion_backup_{timestamp}.json'
        
        filepath = os.path.join('data', filename)
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'version': '1.0',
            'wardrobe': wardrobe,
            'history': history
        }
        
        os.makedirs('data', exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def create_backup_zip(self, wardrobe: Dict, history: list) -> io.BytesIO:
        """
        バックアップZIPファイルを作成
        
        Args:
            wardrobe: ワードローブデータ
            history: 履歴データ
        
        Returns:
            ZIPファイルのバイナリデータ
        """
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # ワードローブデータを追加
            wardrobe_json = json.dumps(wardrobe, ensure_ascii=False, indent=2)
            zip_file.writestr('wardrobe.json', wardrobe_json)
            
            # 履歴データを追加
            history_json = json.dumps(history, ensure_ascii=False, indent=2)
            zip_file.writestr('history.json', history_json)
            
            # メタデータを追加
            metadata = {
                'export_date': datetime.now().isoformat(),
                'version': '1.0',
                'total_items': sum(len(items) for items in wardrobe.values()),
                'total_outfits': len(history)
            }
            metadata_json = json.dumps(metadata, ensure_ascii=False, indent=2)
            zip_file.writestr('metadata.json', metadata_json)
        
        zip_buffer.seek(0)
        return zip_buffer


class DataImporter:
    def __init__(self):
        """データインポーターの初期化"""
        pass
    
    def import_from_json(self, json_string: str) -> Dict:
        """
        JSON文字列からデータをインポート
        
        Args:
            json_string: JSON文字列
        
        Returns:
            インポートされたデータ
        """
        try:
            data = json.loads(json_string)
            
            if 'wardrobe' not in data or 'history' not in data:
                raise ValueError("不正なデータ形式です")
            
            return {
                'success': True,
                'wardrobe': data['wardrobe'],
                'history': data['history'],
                'export_date': data.get('export_date'),
                'version': data.get('version')
            }
        
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f"JSONの解析に失敗しました: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"インポートに失敗しました: {str(e)}"
            }
    
    def import_from_file(self, filepath: str) -> Dict:
        """
        ファイルからデータをインポート
        
        Args:
            filepath: ファイルパス
        
        Returns:
            インポートされたデータ
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_string = f.read()
            
            return self.import_from_json(json_string)
        
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'ファイルが見つかりません'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"ファイルの読み込みに失敗しました: {str(e)}"
            }
    
    def import_from_zip(self, zip_data: bytes) -> Dict:
        """
        ZIPファイルからデータをインポート
        
        Args:
            zip_data: ZIPファイルのバイナリデータ
        
        Returns:
            インポートされたデータ
        """
        try:
            zip_buffer = io.BytesIO(zip_data)
            
            with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                # ワードローブデータを読み込み
                wardrobe_json = zip_file.read('wardrobe.json').decode('utf-8')
                wardrobe = json.loads(wardrobe_json)
                
                # 履歴データを読み込み
                history_json = zip_file.read('history.json').decode('utf-8')
                history = json.loads(history_json)
                
                # メタデータを読み込み
                metadata_json = zip_file.read('metadata.json').decode('utf-8')
                metadata = json.loads(metadata_json)
            
            return {
                'success': True,
                'wardrobe': wardrobe,
                'history': history,
                'metadata': metadata
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"ZIPファイルの読み込みに失敗しました: {str(e)}"
            }
    
    def validate_data(self, data: Dict) -> Dict:
        """
        インポートデータの妥当性を検証
        
        Args:
            data: インポートデータ
        
        Returns:
            検証結果
        """
        errors = []
        warnings = []
        
        # ワードローブの検証
        if 'wardrobe' not in data:
            errors.append("ワードローブデータがありません")
        else:
            wardrobe = data['wardrobe']
            required_categories = ['outer', 'top', 'bottom', 'shoes', 'accessories']
            
            for category in required_categories:
                if category not in wardrobe:
                    errors.append(f"カテゴリー '{category}' がありません")
        
        # 履歴の検証
        if 'history' not in data:
            warnings.append("履歴データがありません")
        else:
            history = data['history']
            if not isinstance(history, list):
                errors.append("履歴データの形式が不正です")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
