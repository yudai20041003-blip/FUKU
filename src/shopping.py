"""
ショッピングサイト検索モジュール
各ブランドの公式サイトで類似商品を検索するためのURL生成
"""
from typing import List, Dict


class ShoppingSearcher:
    def __init__(self):
        """
        ショッピング検索システムの初期化
        """
        self.sites = {
            'ユニクロ': {
                'url': 'https://www.uniqlo.com/jp/ja/search',
                'param': 'q',
                'name': 'ユニクロ'
            },
            'GU': {
                'url': 'https://www.gu-global.com/jp/ja/search',
                'param': 'q',
                'name': 'GU'
            },
            'ZOZOTOWN': {
                'url': 'https://zozo.jp/search',
                'param': 'p_keyv',
                'name': 'ZOZOTOWN'
            },
            'ZARA': {
                'url': 'https://www.zara.com/jp/ja/search',
                'param': 'searchTerm',
                'name': 'ZARA'
            },
            'H&M': {
                'url': 'https://www2.hm.com/ja_jp/search-results.html',
                'param': 'q',
                'name': 'H&M'
            },
            '無印良品': {
                'url': 'https://www.muji.com/jp/ja/store/search',
                'param': 'q',
                'name': '無印良品'
            }
        }
    
    def generate_search_urls(self, item_type: str, style: str, color: str = '') -> List[Dict]:
        """
        各サイトの検索URLを生成
        
        Args:
            item_type: アイテムタイプ（例：Tシャツ、パンツ等）
            style: スタイル（例：ストリート、カジュアル等）
            color: 色（オプション）
        
        Returns:
            検索URLのリスト
        """
        results = []
        
        # 検索キーワードを構築
        keywords = [item_type]
        if style:
            keywords.append(style)
        if color:
            keywords.append(color)
        
        search_query = ' '.join(keywords)
        
        for site_key, site_info in self.sites.items():
            url = self._build_search_url(
                site_info['url'],
                site_info['param'],
                search_query
            )
            
            results.append({
                'site': site_info['name'],
                'url': url,
                'query': search_query
            })
        
        return results
    
    def _build_search_url(self, base_url: str, param: str, query: str) -> str:
        """
        検索URLを構築
        
        Args:
            base_url: ベースURL
            param: クエリパラメータ名
            query: 検索クエリ
        
        Returns:
            完全な検索URL
        """
        separator = '&' if '?' in base_url else '?'
        encoded_query = query.replace(' ', '+')
        return f"{base_url}{separator}{param}={encoded_query}"
    
    def suggest_items_for_style(self, style: str, wardrobe: Dict) -> List[Dict]:
        """
        スタイルに基づいて不足しているアイテムを提案
        
        Args:
            style: 目標スタイル
            wardrobe: 現在のワードローブ
        
        Returns:
            推奨購入アイテムのリスト
        """
        style_essentials = {
            'ストリート': {
                'outer': ['オーバーサイズジャケット', 'MA-1', 'コーチジャケット'],
                'top': ['オーバーサイズTシャツ', 'パーカー', 'スウェット'],
                'bottom': ['ワイドパンツ', 'カーゴパンツ', 'テーパードパンツ'],
                'shoes': ['スニーカー', 'ハイカットスニーカー'],
                'accessories': ['キャップ', 'バケットハット', 'バックパック']
            },
            'シティ': {
                'outer': ['テーラードジャケット', 'ステンカラーコート', 'トレンチコート'],
                'top': ['シャツ', 'ニット', 'カーディガン'],
                'bottom': ['スラックス', 'テーパードパンツ', 'チノパン'],
                'shoes': ['レザーシューズ', 'ローファー', 'ブーツ'],
                'accessories': ['トートバッグ', '腕時計', 'マフラー']
            },
            'カジュアル': {
                'outer': ['デニムジャケット', 'ブルゾン', 'カーディガン'],
                'top': ['Tシャツ', 'ロンT', 'シャツ'],
                'bottom': ['ジーンズ', 'チノパン', 'イージーパンツ'],
                'shoes': ['スニーカー', 'スリッポン'],
                'accessories': ['キャンバスバッグ', 'キャップ', 'サングラス']
            },
            'フォーマル': {
                'outer': ['スーツジャケット', 'ブレザー', 'コート'],
                'top': ['ワイシャツ', 'ポロシャツ'],
                'bottom': ['スラックス', 'ドレスパンツ'],
                'shoes': ['革靴', 'ローファー'],
                'accessories': ['ネクタイ', 'ベルト', 'ブリーフケース']
            },
            'アメカジ': {
                'outer': ['デニムジャケット', 'スタジャン', 'ワークジャケット'],
                'top': ['チェックシャツ', 'スウェット', 'Tシャツ'],
                'bottom': ['デニム', 'チノパン', 'カーゴパンツ'],
                'shoes': ['ブーツ', 'スニーカー', 'デッキシューズ'],
                'accessories': ['ベースボールキャップ', 'バンダナ', 'ベルト']
            },
            'モード': {
                'outer': ['ロングコート', 'ライダース', 'デザインジャケット'],
                'top': ['ブラックTシャツ', 'タートルネック', 'レイヤードトップ'],
                'bottom': ['スキニーパンツ', 'ワイドパンツ', 'デザインパンツ'],
                'shoes': ['ブーツ', 'レザーシューズ', 'ハイカットスニーカー'],
                'accessories': ['ハット', 'ストール', 'シルバーアクセ']
            }
        }
        
        essentials = style_essentials.get(style, style_essentials['カジュアル'])
        suggestions = []
        
        for category, essential_items in essentials.items():
            current_items = wardrobe.get(category, [])
            current_names = [item.get('name', '').lower() for item in current_items]
            
            for essential in essential_items:
                # 似たアイテムを持っているかチェック
                has_similar = any(
                    essential.lower() in name or name in essential.lower()
                    for name in current_names
                )
                
                if not has_similar:
                    suggestions.append({
                        'category': category,
                        'item': essential,
                        'reason': f'{style}スタイルの定番アイテム'
                    })
        
        return suggestions
    
    def get_budget_friendly_tips(self) -> List[str]:
        """
        お手頃価格でファッションを楽しむためのティップス
        
        Returns:
            ティップスのリスト
        """
        return [
            'ユニクロやGUの定番アイテムをベースに、トレンドアイテムを少量追加',
            'セール時期を狙って購入（季節の変わり目がお得）',
            'ベーシックカラー（白、黒、グレー、ネイビー）は長く使えて着回しやすい',
            '無印良品はシンプルで質の良いベーシックアイテムが揃う',
            'ZARAは手頃な価格でトレンドアイテムが手に入る',
            'H&Mはコスパの良いファストファッション',
            'ZOZOTOWNのセールやクーポンを活用'
        ]
    
    def get_price_ranges(self) -> Dict[str, str]:
        """
        各ブランドの価格帯情報
        
        Returns:
            ブランド別価格帯
        """
        return {
            'ユニクロ': '¥1,000-¥10,000（定番アイテム中心）',
            'GU': '¥500-¥5,000（プチプラ）',
            'ZOZOTOWN': '¥2,000-¥50,000+（ブランド多数）',
            'ZARA': '¥2,000-¥15,000（トレンド重視）',
            'H&M': '¥1,000-¥8,000（ファストファッション）',
            '無印良品': '¥1,000-¥10,000（シンプル・高品質）'
        }
