"""
コーディネート推奨モジュール
天気、行き先、スタイルに基づいてコーディネートを提案
"""
import random
from typing import Dict, List, Optional


class OutfitRecommender:
    def __init__(self):
        """
        コーディネート推奨システムの初期化
        """
        self.style_keywords = {
            'カジュアル': ['リラックス', 'ナチュラル', 'デイリー', 'デニム', 'Tシャツ'],
            'ストリート': ['オーバーサイズ', 'スニーカー', 'キャップ', 'レイヤード'],
            'シティ': ['スマート', 'クリーン', 'モダン', 'ミニマル', 'シンプル'],
            'フォーマル': ['スーツ', 'ジャケット', 'シャツ', 'パンプス', 'ネクタイ'],
            'アメカジ': ['デニム', 'チェック', 'スウェット', 'ワーク', 'ヴィンテージ'],
            'モード': ['ブラック', 'モノトーン', 'アシンメトリー', 'アート', 'エッジィ']
        }
        
        # おしゃれになるワンポイントアドバイス集
        self.fashion_tips = [
            # 色に関するアドバイス
            "💡 **色使いのコツ**: 全身を3色以内にまとめると、統一感が出てオシャレに見えます",
            "💡 **モノトーンの魔法**: 迷ったら白・黒・グレーの組み合わせ。失敗知らずの鉄板コーデです",
            "💡 **差し色テク**: モノトーンコーデに1点だけ明るい色を入れると、グッと垢抜けます",
            "💡 **同系色でまとめる**: 似た色味で統一すると、こなれ感が出て上級者っぽく見えます",
            "💡 **アースカラーは万能**: ベージュ・カーキ・ブラウンは、どんな色とも相性抜群です",
            
            # シルエットに関するアドバイス
            "💡 **Yラインシルエット**: トップスゆったり×ボトムス細身で、スタイル良く見えます",
            "💡 **Aラインシルエット**: トップス細身×ボトムスゆったりで、リラックス感とバランス◎",
            "💡 **Iラインシルエット**: 上下ともスッキリさせると、大人っぽくスマートな印象に",
            "💡 **メリハリが大事**: 上下どちらかをタイトに、どちらかをゆったりさせると◎",
            
            # サイズ感に関するアドバイス
            "💡 **ジャストサイズの基本**: 肩のラインが合っているかが、一番重要なポイントです",
            "💡 **袖丈にこだわる**: 手首の骨が見える長さが、最もバランスが良く見えます",
            "💡 **パンツの丈感**: 靴に少しかかるくらいが、ちょうどいい長さの目安です",
            "💡 **オーバーサイズは1点まで**: 全身ダボッとすると野暮ったく見えるので注意",
            
            # レイヤードに関するアドバイス
            "💡 **レイヤードの基本**: インナーを少し見せると、奥行きが出てオシャレ度アップ",
            "💡 **長さの違いを活かす**: 重ね着は裾や袖から少し見せるのがポイント",
            "💡 **色のグラデーション**: 内側に明るい色、外側に暗い色で立体感を演出",
            
            # 小物に関するアドバイス
            "💡 **小物で格上げ**: シンプルなコーデも、腕時計やバッグで一気におしゃれに",
            "💡 **靴の重要性**: 足元をキレイに保つだけで、全体の印象が大きく変わります",
            "💡 **バッグは投資価値アリ**: 良いバッグ1つあれば、コーデ全体が引き締まります",
            "💡 **アクセは引き算**: 小物はつけすぎず、1〜2点に絞るのが大人の余裕",
            
            # スタイル別アドバイス
            "💡 **カジュアルの鉄則**: ラフすぎないように、1点だけキレイめアイテムを入れる",
            "💡 **ストリートのコツ**: オーバーサイズは上下のバランスを意識して",
            "💡 **キレイめの秘訣**: 清潔感が命。シワや汚れに気をつけて",
            "💡 **大人カジュアル**: デニムでもダメージなしの方が、上品に決まります",
            
            # 着こなしテクニック
            "💡 **こなれ感の出し方**: 袖をまくる・裾をロールアップすると、抜け感が出ます",
            "💡 **タックインテク**: 前だけインすると、スタイル良く見えて今っぽい",
            "💡 **ボタンの開け方**: シャツは一番上のボタンを開けると、リラックス感UP",
            "💡 **重心を意識**: 暗い色を下半身に持ってくると、引き締まって見えます",
            
            # 季節に関するアドバイス
            "💡 **春の着こなし**: ライトカラーを取り入れて、季節感を演出しましょう",
            "💡 **夏のポイント**: 白やブルーなど爽やかな色で、涼しげな印象に",
            "💡 **秋の深み**: ブラウン・カーキ・ボルドーで大人っぽく",
            "💡 **冬の重ね着**: アウターの中にパーカーを入れるとこなれ感UP",
            
            # 体型カバー
            "💡 **縦ラインを作る**: ストール・ロングカーディガンで縦長効果",
            "💡 **Vネックがおすすめ**: 首元をスッキリ見せて、顔周りが明るく",
            "💡 **ウエストマーク**: ベルトやタックインで腰位置を高く見せる",
            
            # トレンド
            "💡 **トレンドは1点まで**: 流行アイテムは1つだけ取り入れるのが◎",
            "💡 **定番アイテム重視**: トレンドより、自分に似合う定番を見つけよう",
            "💡 **ベーシック7割**: 全体の7割を定番、3割をトレンドや遊びに",
            
            # メンテナンス
            "💡 **清潔感が最優先**: どんなにおしゃれでも、シワや毛玉はNG",
            "💡 **靴のメンテ**: 定期的に磨くと、長く使えて印象も◎",
            "💡 **サイジングチェック**: 体型が変わったら、サイズを見直すタイミング",
            
            # 自信
            "💡 **堂々と着こなす**: 自信を持って着ることが、一番のおしゃれです",
            "💡 **自分らしさを大切に**: トレンドよりも、自分が心地よいスタイルを",
            "💡 **試着は必須**: 必ず試着して、自分に似合うかを確認しよう"
        ]
        
        self.destination_styles = {
            '大学': ['カジュアル', 'ストリート', 'シティ', 'アメカジ'],
            '仕事・オフィス': ['フォーマル', 'シティ', 'ビジネスカジュアル'],
            'デート': ['シティ', 'カジュアル', 'きれいめ'],
            'カフェ・友達と': ['カジュアル', 'ストリート', 'シティ'],
            'ショッピング': ['カジュアル', 'ストリート', 'トレンド'],
            'アウトドア': ['カジュアル', 'スポーツ', 'アクティブ'],
            'パーティー': ['フォーマル', 'モード', 'ドレッシー']
        }
        
        # スタイル画像URL（2024-2025最新トレンド）
        self.style_images = {
            'カジュアル': 'https://sspark.genspark.ai/cfimages?u1=UVUJYBMWy0wtJYfoKmfCP4KzTkgmVd%2BaGidJ1pYWN%2Fgx2ECi6StH%2FaGGQEZvzfXubTJG2DYQ%2BtfLd055KgDOWQgAdBh1bWTsRRRCKmh7I7BszAtjIpkn%2BZsEoPAUpwbCKieShkqwAU2S73MsEe%2FjUmgrZWy9%2FfkunpF2WQcZNtMnMmrp8R6iCWGjo8aT&u2=n%2BosXP5nkDUBgQcL&width=2560',
            'ストリート': 'https://sspark.genspark.ai/cfimages?u1=wn1i8itk4aJnG%2FG361s%2FwZIKRW54XXH%2BjONoNUe1HmVkYChgSza1rC4%2FJfKp2Jyxas0QRAbX9tCG2SbAZoYz8W0oQxUrvgnODn3YfhNHYAixr4fxQnOWwqrvAfTUQDk%3D&u2=VrPcwJC%2FCdbrDJ4N&width=2560',
            'シティ': 'https://sspark.genspark.ai/cfimages?u1=fMqzG3yzdKBl31fYFobACgwMSkUH8gG9Yfcef3oPPswI68ECa9f%2F7FBj4bqS4gxafePZugldFf1KLBx9aFIV2dPzhO%2FOw5aHnzqrt%2BpNBk2sUuAHFqtPuWUqFnEJkxxeUNv1vKCCLRw4xhsQyuygkKOfwwVUuDNSJhdJ8vkijx4QvIMMohr7m%2B34vIrO&u2=AUfITzwKtf1bwkUy&width=2560',
            'フォーマル': 'https://sspark.genspark.ai/cfimages?u1=dMLRhpRIBFPh2%2F8j%2Bsc9qu6%2B05nQ0nCqau%2B0%2FmSsH%2BUgu%2FIx6fSJvpLsAkF6EPh8mHIZC0GS%2FxfaaaEAfYiQlnjt3Xtz4slQJfahix3T8qvK6V5WXvv5BRk3rC6UsdAxR4s%2BzylaFV2zyrvn4b7%2F%2FkOZ5uIep%2BHa0Hdnl9QXNFf35wa%2FKOYiDu4sXV%2Bj80G0QjtF4njBBFTPgnHAy4Z7Tdl47yMj6eymR9VPKwnel1sVe9QblrY1KaW7&u2=ikzPxsCH9SKUysCj&width=2560',
            'アメカジ': 'https://sspark.genspark.ai/cfimages?u1=4tlH6rKFJZoyGKjWAKavD0pQ%2BcuxpE%2BKotj7oWdEuPYKWm3QtOqozZOMb32R2PXLDrIqPu8DKqHTqz8VGRrdsEMJJIoW7bJy%2B1qLcA5Rfo8JRi07uYaRQDA%3D&u2=Lgq%2BP%2BoHxYolFrqS&width=2560',
            'モード': 'https://sspark.genspark.ai/cfimages?u1=h2QIkgFb%2BngdFHAjYOyskPvO%2BUmOqHqdcftgVThB1fFOAdIOtjPja7wHvHGZKp1ioZhxQ1qs3fCIeWdz7GKE5K%2B4gNM8qEYYKtmTqg%3D%3D&u2=b%2F0EBuDnddJUT67P&width=2560'
        }
    
    def recommend_outfit(self,
                        wardrobe: Dict,
                        weather_rec: Dict,
                        destination: str = 'カフェ・友達と',
                        preferred_style: str = 'カジュアル',
                        temperature: float = 20) -> Dict:
        """
        コーディネートを推奨
        
        Args:
            wardrobe: ワードローブデータ
            weather_rec: 天気に基づく推奨
            destination: 行き先
            preferred_style: 好みのスタイル
            temperature: 現在の気温（体感温度）
        
        Returns:
            推奨コーディネート
        """
        outfit = {
            'outer': None,
            'top': None,
            'bottom': None,
            'shoes': None,
            'accessories': [],
            'reasoning': [],
            'temperature': temperature
        }
        
        # 気温に基づく推奨メッセージを追加
        if weather_rec.get('temp_advice'):
            outfit['reasoning'].append(f"🌡️ {weather_rec['temp_advice']}")
        
        # スタイルに合うアイテムをフィルター
        suitable_items = self._filter_by_style(wardrobe, preferred_style)
        
        # 天気に基づいてアウターを選択
        if weather_rec.get('outer'):
            outfit['outer'] = self._select_item(
                suitable_items.get('outer', []),
                weather_rec['outer']
            )
            if outfit['outer']:
                outfit['reasoning'].append(
                    f"🧥 アウター: {outfit['outer']['name']} - {temperature:.0f}°Cに最適"
                )
        else:
            outfit['reasoning'].append(f"🌡️ {temperature:.0f}°C - アウター不要な暖かさです")
        
        # トップスを選択
        outfit['top'] = self._select_item(
            suitable_items.get('top', []),
            weather_rec.get('top', [])
        )
        if outfit['top']:
            outfit['reasoning'].append(
                f"👕 トップス: {outfit['top']['name']} - {preferred_style}スタイル"
            )
        
        # ボトムスを選択
        outfit['bottom'] = self._select_item(
            suitable_items.get('bottom', []),
            weather_rec.get('bottom', [])
        )
        if outfit['bottom']:
            outfit['reasoning'].append(
                f"👖 ボトムス: {outfit['bottom']['name']} - {destination}に適した選択"
            )
        
        # 靴を選択（天気も考慮）
        if suitable_items.get('shoes'):
            # 雨の日は防水性のある靴を優先
            if weather_rec.get('accessories') and '傘' in weather_rec.get('accessories', []):
                waterproof_shoes = [s for s in suitable_items['shoes'] 
                                   if any(kw in s.get('name', '').lower() 
                                         for kw in ['ブーツ', 'レイン', '防水'])]
                outfit['shoes'] = random.choice(waterproof_shoes) if waterproof_shoes else random.choice(suitable_items['shoes'])
            else:
                outfit['shoes'] = random.choice(suitable_items['shoes'])
            outfit['reasoning'].append(
                f"👞 靴: {outfit['shoes']['name']}"
            )
        
        # アクセサリーを選択
        if weather_rec.get('accessories'):
            for acc_type in weather_rec['accessories']:
                matching_acc = self._find_accessory(
                    suitable_items.get('accessories', []),
                    acc_type
                )
                if matching_acc:
                    outfit['accessories'].append(matching_acc)
                    outfit['reasoning'].append(f"✨ {matching_acc['name']} - 天気に応じた小物")
        
        # 追加のノート
        if weather_rec.get('notes'):
            outfit['reasoning'].extend(weather_rec['notes'])
        
        # おしゃれになるワンポイントアドバイスを追加
        outfit['fashion_tip'] = self._get_random_fashion_tip()
        
        return outfit
    
    def _get_random_fashion_tip(self) -> str:
        """
        ランダムにおしゃれアドバイスを1つ選んで返す
        
        Returns:
            おしゃれになるワンポイントアドバイス
        """
        return random.choice(self.fashion_tips)
    
    def recommend_outfit_from_item(self,
                                   wardrobe: Dict,
                                   favorite_item: Dict,
                                   favorite_category: str,
                                   weather_rec: Dict,
                                   destination: str = 'カフェ・友達と',
                                   temperature: float = 20) -> Dict:
        """
        特定のアイテムをベースにコーディネートを推奨
        
        Args:
            wardrobe: ワードローブデータ
            favorite_item: ベースにするお気に入りアイテム
            favorite_category: お気に入りアイテムのカテゴリー
            weather_rec: 天気に基づく推奨
            destination: 行き先
            temperature: 現在の気温（体感温度）
        
        Returns:
            推奨コーディネート
        """
        outfit = {
            'outer': None,
            'top': None,
            'bottom': None,
            'shoes': None,
            'accessories': [],
            'reasoning': [],
            'styling_tips': [],
            'temperature': temperature
        }
        
        # お気に入りアイテムの情報を取得
        fav_style = favorite_item.get('style', 'カジュアル')
        fav_color = favorite_item.get('color', '').lower()
        fav_brand = favorite_item.get('brand', '')
        
        # お気に入りアイテムを outfit に設定
        outfit[favorite_category] = favorite_item
        outfit['reasoning'].append(
            f"💖 {favorite_item['name']} をベースにコーディネートを組みました"
        )
        
        # お気に入りアイテムのスタイルに合うアイテムをフィルター
        suitable_items = self._filter_by_style(wardrobe, fav_style)
        
        # 色の相性を考慮
        complementary_colors = self._get_complementary_colors(fav_color)
        
        # 気温に基づく推奨メッセージ
        if weather_rec.get('temp_advice'):
            outfit['reasoning'].append(f"🌡️ {weather_rec['temp_advice']}")
        
        # お気に入りアイテムがアウターの場合
        if favorite_category == 'outer':
            # トップスを選択（色の相性を考慮）
            outfit['top'] = self._select_matching_item(
                suitable_items.get('top', []),
                complementary_colors,
                fav_style
            )
            if outfit['top']:
                outfit['reasoning'].append(
                    f"👕 {outfit['top']['name']} - {favorite_item['name']}に合わせやすい色です"
                )
            
            # ボトムスを選択
            outfit['bottom'] = self._select_matching_item(
                suitable_items.get('bottom', []),
                complementary_colors,
                fav_style
            )
            if outfit['bottom']:
                outfit['reasoning'].append(
                    f"👖 {outfit['bottom']['name']} - {fav_style}スタイルでまとまります"
                )
            
            # 靴を選択
            outfit['shoes'] = self._select_item(
                suitable_items.get('shoes', []),
                []
            )
            if outfit['shoes']:
                outfit['reasoning'].append(f"👞 {outfit['shoes']['name']}")
        
        # お気に入りアイテムがトップスの場合
        elif favorite_category == 'top':
            # アウターを選択（気温に応じて）
            if weather_rec.get('outer') and temperature < 15:
                outfit['outer'] = self._select_matching_item(
                    suitable_items.get('outer', []),
                    complementary_colors,
                    fav_style
                )
                if outfit['outer']:
                    outfit['reasoning'].append(
                        f"🧥 {outfit['outer']['name']} - {temperature:.0f}°Cに最適"
                    )
            
            # ボトムスを選択（色の相性を優先）
            outfit['bottom'] = self._select_matching_item(
                suitable_items.get('bottom', []),
                complementary_colors,
                fav_style
            )
            if outfit['bottom']:
                outfit['reasoning'].append(
                    f"👖 {outfit['bottom']['name']} - {favorite_item['name']}との相性◎"
                )
            
            # 靴を選択
            outfit['shoes'] = self._select_item(
                suitable_items.get('shoes', []),
                []
            )
            if outfit['shoes']:
                outfit['reasoning'].append(f"👞 {outfit['shoes']['name']}")
        
        # お気に入りアイテムがボトムスの場合
        elif favorite_category == 'bottom':
            # トップスを選択（色の相性を優先）
            outfit['top'] = self._select_matching_item(
                suitable_items.get('top', []),
                complementary_colors,
                fav_style
            )
            if outfit['top']:
                outfit['reasoning'].append(
                    f"👕 {outfit['top']['name']} - {favorite_item['name']}とのバランス◎"
                )
            
            # アウターを選択（気温に応じて）
            if weather_rec.get('outer') and temperature < 15:
                outfit['outer'] = self._select_matching_item(
                    suitable_items.get('outer', []),
                    complementary_colors,
                    fav_style
                )
                if outfit['outer']:
                    outfit['reasoning'].append(
                        f"🧥 {outfit['outer']['name']} - {temperature:.0f}°Cに最適"
                    )
            
            # 靴を選択
            outfit['shoes'] = self._select_item(
                suitable_items.get('shoes', []),
                []
            )
            if outfit['shoes']:
                outfit['reasoning'].append(f"👞 {outfit['shoes']['name']}")
        
        # お気に入りアイテムが靴の場合
        elif favorite_category == 'shoes':
            # トップスを選択
            outfit['top'] = self._select_matching_item(
                suitable_items.get('top', []),
                complementary_colors,
                fav_style
            )
            if outfit['top']:
                outfit['reasoning'].append(
                    f"👕 {outfit['top']['name']} - {fav_style}スタイル"
                )
            
            # ボトムスを選択
            outfit['bottom'] = self._select_matching_item(
                suitable_items.get('bottom', []),
                complementary_colors,
                fav_style
            )
            if outfit['bottom']:
                outfit['reasoning'].append(
                    f"👖 {outfit['bottom']['name']} - {favorite_item['name']}との相性◎"
                )
            
            # アウターを選択（気温に応じて）
            if weather_rec.get('outer') and temperature < 15:
                outfit['outer'] = self._select_item(
                    suitable_items.get('outer', []),
                    weather_rec['outer']
                )
                if outfit['outer']:
                    outfit['reasoning'].append(
                        f"🧥 {outfit['outer']['name']} - {temperature:.0f}°Cに最適"
                    )
        
        # アクセサリーの場合は通常のコーディネート生成
        elif favorite_category == 'accessories':
            outfit['accessories'].append(favorite_item)
            
            # 他のアイテムを通常通り選択
            outfit['top'] = self._select_item(
                suitable_items.get('top', []),
                weather_rec.get('top', [])
            )
            outfit['bottom'] = self._select_item(
                suitable_items.get('bottom', []),
                weather_rec.get('bottom', [])
            )
            outfit['shoes'] = self._select_item(
                suitable_items.get('shoes', []),
                []
            )
            
            if weather_rec.get('outer') and temperature < 15:
                outfit['outer'] = self._select_item(
                    suitable_items.get('outer', []),
                    weather_rec['outer']
                )
        
        # スタイリングのコツを追加
        styling_tips = self._generate_styling_tips(
            favorite_item,
            favorite_category,
            outfit,
            fav_style
        )
        outfit['styling_tips'] = styling_tips
        
        # 追加のノート
        if weather_rec.get('notes'):
            outfit['reasoning'].extend(weather_rec['notes'])
        
        # おしゃれになるワンポイントアドバイスを追加
        outfit['fashion_tip'] = self._get_random_fashion_tip()
        
        return outfit
    
    def _get_complementary_colors(self, color: str) -> List[str]:
        """
        指定された色に合う色を返す
        
        Args:
            color: 基準となる色
        
        Returns:
            相性の良い色のリスト
        """
        color = color.lower()
        
        color_combinations = {
            '黒': ['白', 'ホワイト', 'グレー', 'ベージュ', 'デニム', 'ブルー', 'カーキ'],
            'ブラック': ['白', 'ホワイト', 'グレー', 'ベージュ', 'デニム', 'ブルー', 'カーキ'],
            '白': ['黒', 'ブラック', 'グレー', 'ネイビー', 'ベージュ', 'デニム', 'ブルー'],
            'ホワイト': ['黒', 'ブラック', 'グレー', 'ネイビー', 'ベージュ', 'デニム', 'ブルー'],
            'グレー': ['白', 'ホワイト', '黒', 'ブラック', 'ネイビー', 'デニム', 'ブルー'],
            'ネイビー': ['白', 'ホワイト', 'グレー', 'ベージュ', 'ブラウン'],
            '紺': ['白', 'ホワイト', 'グレー', 'ベージュ', 'ブラウン'],
            'デニム': ['白', 'ホワイト', '黒', 'ブラック', 'グレー', 'ベージュ'],
            'ブルー': ['白', 'ホワイト', '黒', 'ブラック', 'グレー', 'ベージュ'],
            'ベージュ': ['白', 'ホワイト', 'ネイビー', '紺', 'ブラウン', 'グレー'],
            'ブラウン': ['ベージュ', 'ホワイト', '白', 'グレー', 'カーキ'],
            'カーキ': ['黒', 'ブラック', '白', 'ホワイト', 'ベージュ', 'ブラウン'],
        }
        
        # 色の組み合わせを取得
        for key in color_combinations:
            if key in color:
                return color_combinations[key]
        
        # デフォルトは無難な色
        return ['白', 'ホワイト', '黒', 'ブラック', 'グレー', 'ネイビー']
    
    def _select_matching_item(self,
                             items: List[Dict],
                             complementary_colors: List[str],
                             style: str) -> Optional[Dict]:
        """
        色の相性とスタイルを考慮してアイテムを選択
        
        Args:
            items: アイテムリスト
            complementary_colors: 相性の良い色のリスト
            style: スタイル
        
        Returns:
            選択されたアイテム
        """
        if not items:
            return None
        
        # 色が一致するアイテムを優先
        matching_color_items = []
        for item in items:
            item_color = item.get('color', '').lower()
            for comp_color in complementary_colors:
                if comp_color.lower() in item_color:
                    matching_color_items.append(item)
                    break
        
        # 色が一致するアイテムがあればそこから選択
        if matching_color_items:
            return random.choice(matching_color_items)
        
        # なければ通常通り選択
        return random.choice(items)
    
    def _generate_styling_tips(self,
                              favorite_item: Dict,
                              category: str,
                              outfit: Dict,
                              style: str) -> List[str]:
        """
        スタイリングのコツを生成
        
        Args:
            favorite_item: お気に入りアイテム
            category: カテゴリー
            outfit: コーディネート
            style: スタイル
        
        Returns:
            スタイリングのコツのリスト
        """
        tips = []
        
        fav_name = favorite_item.get('name', '')
        fav_color = favorite_item.get('color', '')
        
        # カテゴリー別のアドバイス
        if category == 'outer':
            tips.append(f"💡 {fav_name}を主役にするため、インナーはシンプルな色味がおすすめです")
            if outfit.get('top'):
                tips.append(f"👕 {outfit['top']['name']}とのレイヤードで奥行きを出しましょう")
        
        elif category == 'top':
            tips.append(f"💡 {fav_name}を活かすため、ボトムスは落ち着いた色味を選びました")
            if '柄' in fav_name or 'プリント' in fav_name:
                tips.append(f"🎨 柄物トップスには無地のボトムスを合わせるのが鉄則です")
        
        elif category == 'bottom':
            tips.append(f"💡 {fav_name}に合わせて、トップスはバランスの取れるものを選びました")
            if 'ワイド' in fav_name or 'wide' in fav_name.lower():
                tips.append(f"👕 ワイドパンツには、コンパクトなトップスでバランスを取りましょう")
        
        elif category == 'shoes':
            tips.append(f"💡 {fav_name}を映えさせるため、全体のカラーバランスを意識しました")
        
        # スタイル別のアドバイス
        if style == 'ストリート':
            tips.append(f"🎯 ストリートスタイルは、オーバーサイズとレイヤードがポイントです")
        elif style == 'シティ':
            tips.append(f"🎯 シティスタイルは、シンプルで清潔感のある組み合わせが基本です")
        elif style == 'カジュアル':
            tips.append(f"🎯 カジュアルスタイルは、リラックス感を大切にしましょう")
        
        return tips
    
    def _filter_by_style(self, wardrobe: Dict, style: str) -> Dict:
        """
        スタイルに基づいてアイテムをフィルター
        
        Args:
            wardrobe: ワードローブ
            style: スタイル
        
        Returns:
            フィルターされたワードローブ
        """
        filtered = {}
        
        for category, items in wardrobe.items():
            filtered[category] = [
                item for item in items
                if style.lower() in item.get('style', '').lower()
                or 'ベーシック' in item.get('style', '')
                or not item.get('style')  # スタイル指定なしは全てにマッチ
            ]
        
        return filtered
    
    def _select_item(self, items: List[Dict], preferences: List[str], exclude_ids: List[str] = None) -> Optional[Dict]:
        """
        推奨に基づいてアイテムを選択（履歴を考慮してランダムに選択）
        
        Args:
            items: アイテムリスト
            preferences: 推奨アイテムタイプのリスト
            exclude_ids: 除外するアイテムのIDリスト（最近使ったアイテム）
        
        Returns:
            選択されたアイテム、なければNone
        """
        if not items:
            return None
        
        # 除外リストがあれば、それを除いたアイテムから選択
        if exclude_ids:
            available_items = [item for item in items if item.get('id') not in exclude_ids]
            # 除外後にアイテムがなければ、除外なしで選択
            if not available_items:
                available_items = items
        else:
            available_items = items
        
        # 推奨に合うアイテムを探す
        matching_items = []
        for pref in preferences:
            matching = [
                item for item in available_items
                if pref.lower() in item.get('name', '').lower()
            ]
            matching_items.extend(matching)
        
        # 推奨に合うものがあればその中からランダムに選択
        if matching_items:
            return random.choice(matching_items)
        
        # 推奨に合うものがなければ全てからランダムに選択
        return random.choice(available_items) if available_items else None
    
    def _find_accessory(self, accessories: List[Dict], acc_type: str) -> Optional[Dict]:
        """
        アクセサリータイプに合うアイテムを探す
        
        Args:
            accessories: アクセサリーリスト
            acc_type: アクセサリータイプ
        
        Returns:
            マッチしたアクセサリー、なければNone
        """
        for acc in accessories:
            if acc_type.lower() in acc.get('name', '').lower():
                return acc
        return None
    
    def generate_pinterest_search_url(self, outfit: Dict, style: str) -> str:
        """
        Pinterestの検索URLを生成
        
        Args:
            outfit: コーディネート
            style: スタイル
        
        Returns:
            Pinterest検索URL
        """
        # コーディネートに基づいてキーワードを生成
        keywords = [style, 'コーデ', 'ファッション']
        
        if outfit.get('top'):
            keywords.append(outfit['top']['name'])
        if outfit.get('bottom'):
            keywords.append(outfit['bottom']['name'])
        
        query = ' '.join(keywords)
        return f"https://www.pinterest.jp/search/pins/?q={query.replace(' ', '%20')}"
    
    def generate_instagram_search_url(self, style: str) -> str:
        """
        Instagramの検索URLを生成
        
        Args:
            style: スタイル
        
        Returns:
            Instagram検索URL
        """
        hashtag = f"{style}コーデ".replace(' ', '')
        return f"https://www.instagram.com/explore/tags/{hashtag}/"
    
    def get_style_description(self, style: str) -> Dict:
        """
        スタイルの詳細な説明を取得
        
        Args:
            style: スタイル名
        
        Returns:
            スタイルの詳細な説明（テキストと画像URL）を含むDict
        """
        descriptions = {
            'カジュアル': '''
**【カジュアルスタイル】**

🎯 **スタイルの特徴**
リラックスした日常的なスタイル。着心地とナチュラルさを重視した、誰でも取り入れやすい定番スタイルです。

👕 **代表的なアイテム**
- **トップス**: Tシャツ、ロンT、パーカー、スウェット、シャツ（ボタンダウン、オックスフォード）
- **アウター**: デニムジャケット、MA-1、コーチジャケット、パーカー
- **ボトムス**: デニムパンツ（ストレート、スリム）、チノパン、カーゴパンツ
- **シューズ**: スニーカー（コンバース、ニューバランス、アディダス）、キャンバスシューズ
- **小物**: キャップ、バックパック、トートバッグ

📌 **こんな人におすすめ**
デイリーユースで動きやすく、どんなシーンでも使える万能スタイルを求める人
''',
            'ストリート': '''
**【ストリートスタイル】**

🎯 **スタイルの特徴**
都市的でトレンド感のあるスタイル。ヒップホップやスケートカルチャーの影響を受けた、個性的で存在感のあるファッションです。

👕 **代表的なアイテム**
- **トップス**: オーバーサイズTシャツ、ロゴ入りスウェット、グラフィックTシャツ、タートルネック
- **アウター**: ビッグシルエットパーカー、MA-1、レザージャケット、ダウンジャケット
- **ボトムス**: ワイドパンツ、ジョガーパンツ、デニムパンツ（ダメージ加工）、スウェットパンツ
- **シューズ**: ハイテクスニーカー（Nike Air Max、Yeezy）、厚底スニーカー、バスケットシューズ
- **小物**: キャップ（フラットバイザー）、チェーンネックレス、ウエストバッグ、バケットハット

📌 **こんな人におすすめ**
個性を出したい、トレンドを取り入れたい、存在感のあるコーディネートを楽しみたい人
''',
            'シティ': '''
**【シティスタイル】**

🎯 **スタイルの特徴**
スマートで洗練された都会的なスタイル。ミニマルで上品な印象を与え、大人の余裕を感じさせるクリーンなファッションです。

👕 **代表的なアイテム**
- **トップス**: 無地シャツ（白、グレー、ネイビー）、ニット（クルーネック、Vネック）、きれいめカットソー
- **アウター**: テーラードジャケット、ステンカラーコート、トレンチコート、シンプルなブルゾン
- **ボトムス**: スラックス（テーパード）、きれいめデニム（濃紺、黒）、チノパン（細身）
- **シューズ**: レザーシューズ、ローファー、シンプルなスニーカー（白、黒）、チェルシーブーツ
- **小物**: レザーバッグ、トートバッグ、シンプルな腕時計、カードケース

📌 **こんな人におすすめ**
デート、カフェ、ちょっとしたお出かけなど、きれいめに決めたいシーンが多い人
''',
            'フォーマル': '''
**【フォーマルスタイル】**

🎯 **スタイルの特徴**
ビジネスやフォーマルシーンに適した格式あるスタイル。信頼感と誠実さを印象づける、きちんとした装いです。

👕 **代表的なアイテム**
- **トップス**: ドレスシャツ（白、サックスブルー）、Yシャツ、ポロシャツ（ビジネスカジュアル）
- **アウター**: スーツジャケット（紺、グレー、黒）、ブレザー、フォーマルコート
- **ボトムス**: スラックス（ウール、ポリエステル）、スーツパンツ、チノパン（ビジネスカジュアル）
- **シューズ**: 革靴（ストレートチップ、プレーントゥ）、ローファー、ダービーシューズ
- **小物**: ネクタイ、レザーベルト、ビジネスバッグ、カフス、革製腕時計

📌 **こんな人におすすめ**
仕事、冠婚葬祭、面接など、フォーマルな場面で適切な服装が求められる人
''',
            'アメカジ': '''
**【アメカジスタイル】**

🎯 **スタイルの特徴**
アメリカンカジュアル。ワークウェアやミリタリーをベースにした、タフでヴィンテージ感のあるカジュアルスタイルです。

👕 **代表的なアイテム**
- **トップス**: チェックシャツ（ネルシャツ、フランネル）、ヘンリーネック、無地Tシャツ、ポケットTシャツ
- **アウター**: デニムジャケット（Gジャン）、ワークジャケット、MA-1、レザージャケット、スタジャン
- **ボトムス**: デニムパンツ（リーバイス501など）、カーゴパンツ、ミリタリーパンツ、ペインターパンツ
- **シューズ**: ワークブーツ（レッドウィング）、コンバース、エンジニアブーツ、スニーカー
- **小物**: キャップ、バンダナ、レザーベルト、デニムバッグ、ミリタリーウォッチ

📌 **こんな人におすすめ**
ヴィンテージやワークウェアが好き、無骨でタフなスタイルを楽しみたい人
''',
            'モード': '''
**【モードスタイル】**

🎯 **スタイルの特徴**
ファッション性の高いアーティスティックなスタイル。モノトーンを基調とし、デザイン性やシルエットで個性を表現する前衛的なファッションです。

👕 **代表的なアイテム**
- **トップス**: モノトーンシャツ（黒、白、グレー）、デザインニット、アシンメトリーカットソー、タートルネック
- **アウター**: ロングコート、モッズコート、オーバーサイズジャケット、レイヤードコート
- **ボトムス**: ワイドパンツ（黒）、テーパードパンツ、サルエルパンツ、スキニーパンツ（黒）
- **シューズ**: レザーブーツ（黒）、ドレスシューズ、デザイナーズスニーカー、ハイカットシューズ
- **小物**: モノトーンバッグ、ハット、マフラー、レザーグローブ、デザイナーズアクセサリー

📌 **こんな人におすすめ**
ファッションを芸術として楽しみたい、他とは違う個性的なスタイルを追求したい人
'''
        }
        
        return {
            'description': descriptions.get(style, 'スタイリッシュなコーディネート'),
            'image_url': self.style_images.get(style, '')
        }
    
    def get_item_compatibility(self, item: Dict) -> Dict:
        """
        アイテムの相性情報を取得
        
        Args:
            item: アイテム情報
        
        Returns:
            相性情報（スタイル、組み合わせアイテム）
        """
        item_name = item.get('name', '').lower()
        item_color = item.get('color', '').lower()
        item_style = item.get('style', '').lower()
        
        # アイテム名から相性の良いスタイルを判定
        compatible_styles = []
        
        # カジュアルスタイルと相性が良いアイテム
        casual_keywords = ['tシャツ', 'デニム', 'ジーンズ', 'スニーカー', 'パーカー', 'スウェット', 'チノパン']
        if any(keyword in item_name for keyword in casual_keywords):
            compatible_styles.append('カジュアル')
        
        # ストリートスタイルと相性が良いアイテム
        street_keywords = ['オーバーサイズ', 'ビッグ', 'ワイド', 'キャップ', 'グラフィック', 'ロゴ', 'スウェット']
        if any(keyword in item_name for keyword in street_keywords):
            compatible_styles.append('ストリート')
        
        # シティスタイルと相性が良いアイテム
        city_keywords = ['シャツ', 'ジャケット', 'スラックス', 'ローファー', 'ニット', 'きれいめ', 'シンプル']
        if any(keyword in item_name for keyword in city_keywords):
            compatible_styles.append('シティ')
        
        # フォーマルスタイルと相性が良いアイテム
        formal_keywords = ['スーツ', 'ジャケット', 'ブレザー', 'ネクタイ', 'ドレス', '革靴', 'レザー']
        if any(keyword in item_name for keyword in formal_keywords):
            compatible_styles.append('フォーマル')
        
        # アメカジスタイルと相性が良いアイテム
        amecaji_keywords = ['デニム', 'ジーンズ', 'チェック', 'ネル', 'ワーク', 'ブーツ', 'ヴィンテージ']
        if any(keyword in item_name for keyword in amecaji_keywords):
            compatible_styles.append('アメカジ')
        
        # モードスタイルと相性が良いアイテム
        mode_keywords = ['ブラック', 'モノトーン', 'ロング', 'ワイド', 'デザイン']
        if any(keyword in item_name for keyword in mode_keywords):
            compatible_styles.append('モード')
        
        # スタイル情報がある場合は追加
        if item_style and item_style != 'ベーシック':
            for style in ['カジュアル', 'ストリート', 'シティ', 'フォーマル', 'アメカジ', 'モード']:
                if style.lower() in item_style and style not in compatible_styles:
                    compatible_styles.append(style)
        
        # 相性の良いアイテムの推奨
        matching_items = self._get_matching_items(item)
        
        return {
            'compatible_styles': compatible_styles if compatible_styles else ['カジュアル', 'ベーシック'],
            'matching_items': matching_items
        }
    
    def _get_matching_items(self, item: Dict) -> Dict:
        """
        アイテムと組み合わせやすいアイテムを取得
        
        Args:
            item: アイテム情報
        
        Returns:
            組み合わせやすいアイテムの辞書
        """
        item_name = item.get('name', '').lower()
        item_color = item.get('color', '').lower()
        
        matching = {
            'tops': [],
            'bottoms': [],
            'outers': [],
            'shoes': [],
            'tips': []
        }
        
        # Tシャツ・カットソー
        if 'tシャツ' in item_name or 'カットソー' in item_name:
            matching['bottoms'] = ['デニムパンツ', 'チノパン', 'ワイドパンツ', 'ショートパンツ']
            matching['outers'] = ['デニムジャケット', 'パーカー', 'カーディガン', 'MA-1']
            matching['shoes'] = ['スニーカー', 'キャンバスシューズ']
            matching['tips'].append('ベーシックなアイテムなので、ボトムスやアウターで個性を出しましょう')
        
        # シャツ
        elif 'シャツ' in item_name:
            matching['bottoms'] = ['スラックス', 'チノパン', 'デニム（濃紺）', 'きれいめパンツ']
            matching['outers'] = ['ジャケット', 'カーディガン', 'ニット（重ね着）']
            matching['shoes'] = ['レザーシューズ', 'ローファー', 'きれいめスニーカー']
            matching['tips'].append('襟付きシャツはきちんと感が出るので、きれいめなボトムスと合わせましょう')
        
        # ニット・セーター
        elif 'ニット' in item_name or 'セーター' in item_name:
            matching['bottoms'] = ['スラックス', 'デニム', 'チノパン', 'ワイドパンツ']
            matching['tops'] = ['シャツ（インナー）', 'タートルネック（インナー）']
            matching['shoes'] = ['レザーシューズ', 'スニーカー', 'ブーツ']
            matching['tips'].append('シャツと重ね着すると上品な印象に。単体でも存在感があります')
        
        # デニムパンツ
        elif 'デニム' in item_name or 'ジーンズ' in item_name:
            matching['tops'] = ['Tシャツ', 'シャツ', 'パーカー', 'ニット', 'スウェット']
            matching['outers'] = ['ジャケット', 'パーカー', 'コート', 'MA-1']
            matching['shoes'] = ['スニーカー', 'ブーツ', 'レザーシューズ']
            matching['tips'].append('万能アイテム！どんなトップスとも相性が良く、カジュアルからきれいめまで対応')
        
        # スラックス
        elif 'スラックス' in item_name or 'パンツ' in item_name:
            matching['tops'] = ['シャツ', 'ニット', 'カットソー', 'ポロシャツ']
            matching['outers'] = ['ジャケット', 'コート', 'カーディガン']
            matching['shoes'] = ['レザーシューズ', 'ローファー', 'きれいめスニーカー']
            matching['tips'].append('きちんと感のあるアイテム。シャツやジャケットと合わせて大人の雰囲気に')
        
        # ジャケット
        elif 'ジャケット' in item_name:
            matching['tops'] = ['シャツ', 'ニット', 'Tシャツ', 'カットソー']
            matching['bottoms'] = ['スラックス', 'チノパン', 'きれいめデニム']
            matching['shoes'] = ['レザーシューズ', 'ローファー', 'きれいめスニーカー']
            matching['tips'].append('コーディネートの格上げアイテム。インナーとボトムスをシンプルにまとめましょう')
        
        # パーカー
        elif 'パーカー' in item_name:
            matching['bottoms'] = ['デニム', 'スウェットパンツ', 'チノパン', 'ワイドパンツ']
            matching['outers'] = ['デニムジャケット', 'MA-1', 'コーチジャケット']
            matching['shoes'] = ['スニーカー', 'キャンバスシューズ']
            matching['tips'].append('カジュアルの定番。オーバーサイズだとストリート、ジャストサイズならカジュアルに')
        
        # スニーカー
        elif 'スニーカー' in item_name:
            matching['tops'] = ['Tシャツ', 'パーカー', 'シャツ', 'ニット']
            matching['bottoms'] = ['デニム', 'チノパン', 'スウェットパンツ', 'ショートパンツ']
            matching['tips'].append('カジュアルスタイルの必需品。白スニーカーは特に万能で清潔感がアップ')
        
        # レザーシューズ・革靴
        elif 'レザー' in item_name or '革靴' in item_name or 'ローファー' in item_name:
            matching['tops'] = ['シャツ', 'ニット', 'ジャケット']
            matching['bottoms'] = ['スラックス', 'チノパン', 'きれいめデニム']
            matching['tips'].append('きちんと感を出す重要アイテム。パンツの裾は革靴に軽く触れる程度が理想')
        
        # 色の組み合わせアドバイス（汎用性とバランスを重視）
        if '白' in item_color or 'ホワイト' in item_color:
            matching['tips'].append('🎨 **色の組み合わせ**: 白はどんな色とも合わせやすい万能カラー。清潔感があり、明るいコーデの基本に')
            matching['tips'].append('💡 **おしゃれに見せるコツ**: 全身を3色以内にまとめると統一感が出ます。白を差し色として使うのもおすすめ')
        elif '黒' in item_color or 'ブラック' in item_color:
            matching['tips'].append('🎨 **色の組み合わせ**: 黒は引き締め効果抜群。他の色を引き立てる役割も。グレーや白との相性が特に良い')
            matching['tips'].append('💡 **おしゃれに見せるコツ**: 黒ばかりにならないように、1点だけ明るい色を入れるとバランスが良くなります')
        elif 'ネイビー' in item_color or '紺' in item_color:
            matching['tips'].append('🎨 **色の組み合わせ**: ネイビーは上品で使いやすい。白、グレー、ベージュ、茶色と好相性')
            matching['tips'].append('💡 **おしゃれに見せるコツ**: 黒よりも柔らかい印象に。同系色でまとめると洗練された雰囲気に')
        elif 'ベージュ' in item_color or 'キャメル' in item_color or 'ブラウン' in item_color or '茶' in item_color:
            matching['tips'].append('🎨 **色の組み合わせ**: ベージュ・茶系は温かみのある印象。白、黒、ネイビーと相性抜群')
            matching['tips'].append('💡 **おしゃれに見せるコツ**: アースカラー同士（ベージュ、ブラウン、カーキ）の組み合わせで統一感が出ます')
        elif 'グレー' in item_color or '灰色' in item_color:
            matching['tips'].append('🎨 **色の組み合わせ**: グレーは中間色で合わせやすい。白・黒・ネイビー・ピンクなど幅広く対応')
            matching['tips'].append('💡 **おしゃれに見せるコツ**: 濃淡の異なるグレーを組み合わせるグラデーションコーデもおしゃれ')
        elif any(color in item_color for color in ['赤', 'レッド', '青', 'ブルー', '緑', 'グリーン', '黄', 'イエロー']):
            matching['tips'].append('🎨 **色の組み合わせ**: 鮮やかな色は差し色として活躍。白・黒・ネイビー・グレーなどベーシックカラーと合わせるとバランスが良い')
            matching['tips'].append('💡 **おしゃれに見せるコツ**: ビビッドな色同士は避けて、1点だけアクセントにすると派手すぎず洗練されます')
        
        # 全般的なコーディネートバランスのアドバイス
        if not any('色の組み合わせ' in tip for tip in matching['tips']):
            matching['tips'].append('🎨 **基本ルール**: 全身を3色以内にまとめるとごちゃごちゃせず、すっきりまとまります')
            matching['tips'].append('💡 **配色のコツ**: ベースカラー（60%）、メインカラー（30%）、アクセントカラー（10%）のバランスを意識しましょう')
        
        return matching
    
    def analyze_wardrobe_versatility(self, wardrobe: Dict) -> Dict:
        """
        ワードローブ全体の汎用性を分析
        
        Args:
            wardrobe: ワードローブデータ
        
        Returns:
            汎用性分析結果
        """
        analysis = {
            'versatile_items': [],
            'underused_items': [],
            'missing_basics': [],
            'recommendations': []
        }
        
        # 基本アイテムのチェックリスト
        basics = {
            'outer': ['ジャケット', 'デニムジャケット', 'カーディガン'],
            'top': ['白Tシャツ', 'シャツ', 'ニット'],
            'bottom': ['デニムパンツ', '黒パンツ', 'チノパン'],
            'shoes': ['白スニーカー', '革靴', 'ローファー']
        }
        
        # 各カテゴリーをチェック
        for category, basic_list in basics.items():
            existing_items = [item.get('name', '').lower() for item in wardrobe.get(category, [])]
            for basic in basic_list:
                found = False
                for existing in existing_items:
                    if basic.lower() in existing:
                        found = True
                        break
                if not found:
                    analysis['missing_basics'].append({
                        'category': category,
                        'item': basic,
                        'reason': f'{basic}は様々なスタイルに使える万能アイテムです'
                    })
        
        # 汎用性の高いアイテムを特定
        for category, items in wardrobe.items():
            for item in items:
                versatility_score = self._calculate_item_versatility(item)
                if versatility_score >= 7:
                    analysis['versatile_items'].append({
                        'item': item,
                        'score': versatility_score,
                        'category': category
                    })
        
        # レコメンデーションを生成
        if len(analysis['missing_basics']) > 0:
            analysis['recommendations'].append({
                'priority': '高',
                'title': '基本アイテムを揃えましょう',
                'description': f"{len(analysis['missing_basics'])}個の基本アイテムが不足しています。これらを揃えることで、コーディネートの幅が大きく広がります。"
            })
        
        return analysis
    
    def _calculate_item_versatility(self, item: Dict) -> int:
        """
        アイテムの汎用性スコアを計算（内部用）
        
        Args:
            item: アイテム情報
        
        Returns:
            汎用性スコア（1-10）
        """
        score = 5  # 基本スコア
        
        # 色による評価
        color = item.get('color', '').lower()
        neutral_colors = ['黒', 'ブラック', '白', 'ホワイト', 'グレー', 'ネイビー', '紺', 'ベージュ']
        if any(nc in color for nc in neutral_colors):
            score += 2
        
        # スタイルによる評価
        style = item.get('style', '').lower()
        if 'ベーシック' in style or 'カジュアル' in style:
            score += 1
        
        # 季節による評価
        season = item.get('season', '')
        if isinstance(season, str):
            seasons = season.split(',')
            if len(seasons) >= 3:
                score += 2
        
        return min(score, 10)
    
    def suggest_additions_for_style(self, wardrobe: Dict, target_style: str, weather_temp: float = 20) -> Dict:
        """
        特定のスタイルに必要なアイテムを提案
        
        Args:
            wardrobe: 現在のワードローブ
            target_style: 目標とするスタイル
            weather_temp: 現在の気温
        
        Returns:
            提案アイテムリスト
        """
        suggestions = {
            'essential': [],
            'nice_to_have': [],
            'seasonal': []
        }
        
        # スタイル別の必須アイテム
        style_essentials = {
            'カジュアル': {
                'outer': ['デニムジャケット', 'パーカー'],
                'top': ['白Tシャツ', 'ロンT', 'シャツ'],
                'bottom': ['デニムパンツ', 'チノパン'],
                'shoes': ['スニーカー']
            },
            'ストリート': {
                'outer': ['オーバーサイズパーカー', 'MA-1'],
                'top': ['ビッグTシャツ', 'スウェット'],
                'bottom': ['ワイドパンツ', 'ジョガーパンツ'],
                'shoes': ['ハイテクスニーカー']
            },
            'シティ': {
                'outer': ['テーラードジャケット', 'ステンカラーコート'],
                'top': ['シャツ', 'ニット'],
                'bottom': ['スラックス', 'きれいめデニム'],
                'shoes': ['レザーシューズ', 'ローファー']
            },
            'フォーマル': {
                'outer': ['スーツジャケット'],
                'top': ['ドレスシャツ', 'Yシャツ'],
                'bottom': ['スラックス'],
                'shoes': ['革靴']
            },
            'アメカジ': {
                'outer': ['デニムジャケット', 'ワークジャケット'],
                'top': ['チェックシャツ', 'ヘンリーネック'],
                'bottom': ['デニムパンツ', 'カーゴパンツ'],
                'shoes': ['ワークブーツ']
            },
            'モード': {
                'outer': ['ロングコート', 'オーバーサイズジャケット'],
                'top': ['モノトーンシャツ', 'タートルネック'],
                'bottom': ['ワイドパンツ', 'スキニーパンツ'],
                'shoes': ['レザーブーツ']
            }
        }
        
        if target_style not in style_essentials:
            return suggestions
        
        essentials = style_essentials[target_style]
        
        # 各カテゴリーをチェック
        for category, essential_items in essentials.items():
            existing_items = [item.get('name', '').lower() for item in wardrobe.get(category, [])]
            for essential in essential_items:
                found = False
                for existing in existing_items:
                    if essential.lower() in existing:
                        found = True
                        break
                if not found:
                    suggestions['essential'].append({
                        'category': category,
                        'item': essential,
                        'style': target_style,
                        'reason': f'{target_style}スタイルの定番アイテム'
                    })
        
        # 天気に応じた季節的な提案
        if weather_temp < 10:
            suggestions['seasonal'].append({
                'category': 'outer',
                'item': 'ダウンジャケット or 厚手のコート',
                'reason': f'気温{weather_temp}°C - 防寒対策が必要です'
            })
        elif weather_temp > 25:
            suggestions['seasonal'].append({
                'category': 'top',
                'item': '半袖Tシャツ or ポロシャツ',
                'reason': f'気温{weather_temp}°C - 涼しい服装がおすすめです'
            })
        
        return suggestions
    
    def generate_outfit_preview_prompt(self, suggested_items: List[Dict], 
                                       existing_wardrobe: Dict, 
                                       style: str, 
                                       weather_temp: float = 20) -> str:
        """
        提案アイテムと既存ワードローブを組み合わせたコーディネート画像生成用プロンプト
        
        Args:
            suggested_items: 提案されたアイテムのリスト
            existing_wardrobe: 既存のワードローブ
            style: スタイル
            weather_temp: 気温
        
        Returns:
            画像生成用プロンプト（英語）
        """
        # スタイルの英語表記
        style_map = {
            'カジュアル': 'casual',
            'ストリート': 'streetwear',
            'シティ': 'smart casual',
            'フォーマル': 'formal business',
            'アメカジ': 'American casual',
            'モード': 'avant-garde fashion'
        }
        
        style_en = style_map.get(style, 'casual')
        
        # 提案アイテムを整理
        outfit_items = []
        for item in suggested_items:
            outfit_items.append(item['item'])
        
        # 既存のワードローブから相性の良いアイテムを選択
        complementary_items = []
        for category, items in existing_wardrobe.items():
            if items and len(complementary_items) < 2:
                # 汎用性の高いアイテムを優先
                sorted_items = sorted(items, 
                                    key=lambda x: self._calculate_item_versatility(x), 
                                    reverse=True)
                if sorted_items:
                    item = sorted_items[0]
                    complementary_items.append(f"{item.get('color', '')} {item.get('name', '')}")
        
        # プロンプトを構築
        prompt_parts = [
            f"Japanese male college student {style_en} style outfit coordination.",
            f"Full body shot showing complete outfit.",
        ]
        
        # 提案アイテムを追加
        if outfit_items:
            items_desc = ", ".join(outfit_items[:4])  # 最大4アイテム
            prompt_parts.append(f"Wearing: {items_desc}.")
        
        # 既存アイテムを追加
        if complementary_items:
            comp_desc = " and ".join(complementary_items)
            prompt_parts.append(f"Styled with: {comp_desc}.")
        
        # 気温に応じた説明
        if weather_temp < 10:
            prompt_parts.append("Winter layering with warm outerwear.")
        elif weather_temp < 20:
            prompt_parts.append("Light layering for mild weather.")
        elif weather_temp > 25:
            prompt_parts.append("Light and breathable summer styling.")
        
        # スタイルの特徴を追加
        style_details = {
            'casual': 'Relaxed, comfortable, natural look. Clean and simple coordination.',
            'streetwear': 'Trendy urban fashion with oversized silhouettes and bold styling.',
            'smart casual': 'Sophisticated and polished modern style. Clean minimalist aesthetic.',
            'formal business': 'Professional business attire. Sharp and well-tailored.',
            'American casual': 'Vintage-inspired workwear aesthetic with denim and classic pieces.',
            'avant-garde fashion': 'Artistic monochrome fashion with architectural silhouettes.'
        }
        
        prompt_parts.append(style_details.get(style_en, 'Stylish modern fashion.'))
        prompt_parts.append("Natural lighting, clean background, fashion photography style.")
        
        return " ".join(prompt_parts)
    
    def create_outfit_combination(self, suggested_items: List[Dict], 
                                  existing_wardrobe: Dict,
                                  style: str) -> Dict:
        """
        提案アイテムと既存ワードローブの組み合わせを作成
        
        Args:
            suggested_items: 提案されたアイテム
            existing_wardrobe: 既存のワードローブ
            style: スタイル
        
        Returns:
            組み合わせの詳細
        """
        combination = {
            'new_items': [],
            'existing_items': [],
            'description': '',
            'styling_tips': []
        }
        
        # 提案アイテムをカテゴリー別に整理
        suggested_by_category = {}
        for item in suggested_items:
            cat = item.get('category', 'other')
            if cat not in suggested_by_category:
                suggested_by_category[cat] = []
            suggested_by_category[cat].append(item)
        
        # カテゴリーの優先順位
        category_order = ['outer', 'top', 'bottom', 'shoes', 'accessories']
        
        # 各カテゴリーから選択
        for category in category_order:
            # 提案アイテムがあればそれを使用
            if category in suggested_by_category and suggested_by_category[category]:
                item = suggested_by_category[category][0]
                combination['new_items'].append({
                    'category': category,
                    'name': item['item'],
                    'reason': item.get('reason', ''),
                    'is_new': True
                })
            # なければ既存のワードローブから選択
            elif category in existing_wardrobe and existing_wardrobe[category]:
                # 汎用性の高いアイテムを選択
                sorted_items = sorted(existing_wardrobe[category],
                                    key=lambda x: self._calculate_item_versatility(x),
                                    reverse=True)
                if sorted_items:
                    item = sorted_items[0]
                    combination['existing_items'].append({
                        'category': category,
                        'name': item.get('name', ''),
                        'color': item.get('color', ''),
                        'is_new': False
                    })
        
        # スタイリングのコツを追加
        combination['styling_tips'] = [
            f'💡 {style}スタイルの基本を押さえたコーディネートです',
            '🎨 全体を3色以内にまとめるとバランスが良くなります',
            '✨ 新しいアイテムを取り入れることで、コーディネートの幅が広がります'
        ]
        
        # 説明文を生成
        new_count = len(combination['new_items'])
        existing_count = len(combination['existing_items'])
        combination['description'] = f'提案アイテム{new_count}点 + 手持ちアイテム{existing_count}点の組み合わせ'
        
        return combination
