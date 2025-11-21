"""
コーディネート履歴管理のテスト
"""
import sys
import os
import tempfile

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from history import OutfitHistoryManager


def test_history_initialization():
    """履歴マネージャーの初期化テスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = OutfitHistoryManager(data_file=temp_file)
        assert manager is not None
        assert isinstance(manager.history, list)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_add_outfit():
    """コーディネート追加のテスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = OutfitHistoryManager(data_file=temp_file)
        
        outfit = {
            'outer': {'name': 'デニムジャケット', 'color': 'ブルー'},
            'top': {'name': '白Tシャツ', 'color': 'ホワイト'},
            'bottom': {'name': 'ジーンズ', 'color': 'ブルー'}
        }
        
        weather = {
            'temperature': 20,
            'description': '晴れ',
            'humidity': 60
        }
        
        result = manager.add_outfit(
            outfit, 
            weather, 
            'カフェ・友達と', 
            'カジュアル',
            rating=4
        )
        
        assert result is True
        history = manager.get_history()
        assert len(history) == 1
        assert history[0]['style'] == 'カジュアル'
        assert history[0]['rating'] == 4
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_update_rating():
    """評価更新のテスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = OutfitHistoryManager(data_file=temp_file)
        
        outfit = {'top': {'name': 'テストTシャツ'}}
        weather = {'temperature': 25, 'description': '晴れ', 'humidity': 50}
        
        manager.add_outfit(outfit, weather, 'ショッピング', 'カジュアル', rating=3)
        
        history = manager.get_history()
        outfit_id = history[0]['id']
        
        result = manager.update_rating(outfit_id, 5)
        assert result is True
        
        updated_history = manager.get_history()
        assert updated_history[0]['rating'] == 5
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_statistics():
    """統計情報のテスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = OutfitHistoryManager(data_file=temp_file)
        
        # 複数のコーディネートを追加
        outfits_data = [
            ('カジュアル', 'カフェ・友達と', 4),
            ('カジュアル', 'ショッピング', 5),
            ('ストリート', 'カフェ・友達と', 3),
        ]
        
        for style, dest, rating in outfits_data:
            outfit = {'top': {'name': 'テスト'}}
            weather = {'temperature': 20, 'description': '晴れ', 'humidity': 60}
            manager.add_outfit(outfit, weather, dest, style, rating)
        
        stats = manager.get_statistics()
        
        assert stats['total_outfits'] == 3
        assert stats['most_used_style'] == 'カジュアル'
        assert stats['most_common_destination'] == 'カフェ・友達と'
        assert stats['average_rating'] == 4.0
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_get_favorite_outfits():
    """お気に入りコーディネートの取得テスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = OutfitHistoryManager(data_file=temp_file)
        
        # 異なる評価のコーディネートを追加
        ratings = [2, 3, 4, 5, 5]
        for rating in ratings:
            outfit = {'top': {'name': f'テスト{rating}'}}
            weather = {'temperature': 20, 'description': '晴れ', 'humidity': 60}
            manager.add_outfit(outfit, weather, 'カフェ', 'カジュアル', rating)
        
        favorites = manager.get_favorite_outfits(min_rating=4)
        assert len(favorites) == 3  # 評価4以上は3つ
        
        # 評価の降順でソートされていることを確認
        assert favorites[0]['rating'] >= favorites[-1]['rating']
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == '__main__':
    print("Running history tests...")
    
    test_history_initialization()
    print("✓ Initialization test passed")
    
    test_add_outfit()
    print("✓ Add outfit test passed")
    
    test_update_rating()
    print("✓ Update rating test passed")
    
    test_statistics()
    print("✓ Statistics test passed")
    
    test_get_favorite_outfits()
    print("✓ Get favorite outfits test passed")
    
    print("\nAll tests passed! ✅")
