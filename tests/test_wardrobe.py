"""
ワードローブ管理機能のテスト
"""
import sys
import os
import tempfile
import json

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from wardrobe import WardrobeManager


def test_wardrobe_initialization():
    """ワードローブマネージャーの初期化テスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = WardrobeManager(data_file=temp_file)
        assert manager is not None
        assert isinstance(manager.wardrobe, dict)
        assert 'outer' in manager.wardrobe
        assert 'top' in manager.wardrobe
        assert 'bottom' in manager.wardrobe
        assert 'shoes' in manager.wardrobe
        assert 'accessories' in manager.wardrobe
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_add_item():
    """アイテム追加のテスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = WardrobeManager(data_file=temp_file)
        
        item = {
            'name': 'テストTシャツ',
            'color': 'ホワイト',
            'brand': 'テストブランド',
            'style': 'カジュアル',
            'season': '春,夏'
        }
        
        result = manager.add_item('top', item)
        assert result is True
        
        items = manager.get_items_by_category('top')
        assert len(items) == 1
        assert items[0]['name'] == 'テストTシャツ'
        assert 'id' in items[0]
        assert 'added_date' in items[0]
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_remove_item():
    """アイテム削除のテスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = WardrobeManager(data_file=temp_file)
        
        item = {
            'name': 'テストジャケット',
            'color': 'ブラック',
            'brand': 'テストブランド',
            'style': 'シティ',
            'season': '秋,冬'
        }
        
        manager.add_item('outer', item)
        items_before = manager.get_items_by_category('outer')
        assert len(items_before) == 1
        
        item_id = items_before[0]['id']
        result = manager.remove_item('outer', item_id)
        assert result is True
        
        items_after = manager.get_items_by_category('outer')
        assert len(items_after) == 0
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_search_items():
    """アイテム検索のテスト"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        manager = WardrobeManager(data_file=temp_file)
        
        # テストデータを追加
        manager.add_item('top', {
            'name': '白Tシャツ',
            'color': 'ホワイト',
            'brand': 'ユニクロ',
            'style': 'カジュアル',
            'season': '春,夏'
        })
        
        manager.add_item('top', {
            'name': '黒Tシャツ',
            'color': 'ブラック',
            'brand': 'GU',
            'style': 'ストリート',
            'season': '春,夏,秋'
        })
        
        # 色で検索
        results = manager.search_items(color='ホワイト')
        assert len(results) == 1
        assert results[0]['name'] == '白Tシャツ'
        
        # スタイルで検索
        results = manager.search_items(style='ストリート')
        assert len(results) == 1
        assert results[0]['name'] == '黒Tシャツ'
        
        # キーワードで検索
        results = manager.search_items(keywords='Tシャツ')
        assert len(results) == 2
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_sample_wardrobe():
    """サンプルワードローブのテスト"""
    manager = WardrobeManager()
    sample = manager.get_sample_wardrobe()
    
    assert isinstance(sample, dict)
    assert 'outer' in sample
    assert 'top' in sample
    assert 'bottom' in sample
    assert 'shoes' in sample
    assert 'accessories' in sample
    
    assert len(sample['outer']) > 0
    assert len(sample['top']) > 0
    assert len(sample['bottom']) > 0


if __name__ == '__main__':
    print("Running wardrobe tests...")
    test_wardrobe_initialization()
    print("✓ Initialization test passed")
    
    test_add_item()
    print("✓ Add item test passed")
    
    test_remove_item()
    print("✓ Remove item test passed")
    
    test_search_items()
    print("✓ Search items test passed")
    
    test_sample_wardrobe()
    print("✓ Sample wardrobe test passed")
    
    print("\nAll tests passed! ✅")
