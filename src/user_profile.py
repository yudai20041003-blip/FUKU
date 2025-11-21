"""
ユーザープロフィール管理モジュール
身長・体重などのユーザー情報を管理し、サイズ推奨を行う
"""
import json
import os
from typing import Dict, Optional


class UserProfileManager:
    def __init__(self, data_file: str = "data/user_profile.json"):
        """
        ユーザープロフィール管理の初期化
        
        Args:
            data_file: データファイルのパス
        """
        self.data_file = data_file
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """プロフィールをファイルから読み込む"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"プロフィールの読み込みに失敗: {e}")
        
        # デフォルトプロフィール
        return {
            'height': None,  # 身長（cm）
            'weight': None,  # 体重（kg）
            'age': None,     # 年齢
            'preferred_fit': 'regular'  # ジャストサイズ or オーバーサイズ
        }
    
    def _save_profile(self) -> bool:
        """プロフィールをファイルに保存"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"プロフィールの保存に失敗: {e}")
            return False
    
    def update_profile(self, height: Optional[int] = None, 
                      weight: Optional[int] = None,
                      age: Optional[int] = None,
                      preferred_fit: Optional[str] = None) -> bool:
        """
        プロフィールを更新
        
        Args:
            height: 身長（cm）
            weight: 体重（kg）
            age: 年齢
            preferred_fit: 好みのフィット感
        
        Returns:
            更新成功時True
        """
        if height is not None:
            self.profile['height'] = height
        if weight is not None:
            self.profile['weight'] = weight
        if age is not None:
            self.profile['age'] = age
        if preferred_fit is not None:
            self.profile['preferred_fit'] = preferred_fit
        
        return self._save_profile()
    
    def get_profile(self) -> Dict:
        """現在のプロフィールを取得"""
        return self.profile.copy()
    
    def calculate_bmi(self) -> Optional[float]:
        """BMIを計算"""
        height = self.profile.get('height')
        weight = self.profile.get('weight')
        
        if height and weight:
            height_m = height / 100.0
            return round(weight / (height_m ** 2), 1)
        return None
    
    def get_body_type(self) -> str:
        """
        体型を判定
        
        Returns:
            体型（痩せ型/標準/ややぽっちゃり/ぽっちゃり）
        """
        bmi = self.calculate_bmi()
        if bmi is None:
            return "未設定"
        
        if bmi < 18.5:
            return "痩せ型"
        elif bmi < 23:
            return "標準"
        elif bmi < 25:
            return "ややぽっちゃり"
        else:
            return "ぽっちゃり"
    
    def get_size_recommendation(self, category: str = 'top') -> Dict:
        """
        カテゴリー別のサイズ推奨を取得
        
        Args:
            category: カテゴリー（top/bottom/shoes）
        
        Returns:
            サイズ推奨情報
        """
        height = self.profile.get('height')
        weight = self.profile.get('weight')
        preferred_fit = self.profile.get('preferred_fit', 'regular')
        
        if not height or not weight:
            return {
                'size': '未設定',
                'advice': '身長・体重を設定すると、おすすめのサイズが表示されます'
            }
        
        bmi = self.calculate_bmi()
        body_type = self.get_body_type()
        
        recommendation = {
            'body_type': body_type,
            'bmi': bmi,
            'sizes': {},
            'advice': []
        }
        
        # トップスのサイズ推奨
        if category == 'top':
            if height < 165:
                base_size = 'S'
            elif height < 175:
                base_size = 'M'
            elif height < 185:
                base_size = 'L'
            else:
                base_size = 'XL'
            
            # BMIに応じて調整
            if bmi > 25:
                if base_size == 'S':
                    base_size = 'M'
                elif base_size == 'M':
                    base_size = 'L'
                elif base_size == 'L':
                    base_size = 'XL'
            
            # フィット感の好みに応じて調整
            if preferred_fit == 'oversized':
                recommendation['sizes']['recommended'] = f'{base_size}～XL（オーバーサイズ）'
                recommendation['advice'].append('💡 オーバーサイズで今っぽく着こなすなら、ワンサイズ大きめがおすすめ')
            else:
                recommendation['sizes']['recommended'] = base_size
                recommendation['advice'].append(f'💡 身長{height}cm、体型{body_type}の方には{base_size}サイズがおすすめです')
            
            # 体型別のアドバイス
            if body_type == '痩せ型':
                recommendation['advice'].append('✨ レイヤードスタイルで立体感を出すとバランスが良くなります')
            elif body_type == 'ぽっちゃり':
                recommendation['advice'].append('✨ ゆったりめのシルエットで体型をカバーしつつ、おしゃれに')
        
        # ボトムスのサイズ推奨
        elif category == 'bottom':
            # ウエストサイズの推定（簡易的）
            if bmi < 20:
                waist_range = '28～30'
            elif bmi < 23:
                waist_range = '30～32'
            elif bmi < 25:
                waist_range = '32～34'
            else:
                waist_range = '34～36'
            
            # 股下の推定
            inseam = int(height * 0.45)
            
            recommendation['sizes']['waist'] = f'{waist_range}インチ'
            recommendation['sizes']['inseam'] = f'{inseam}cm'
            recommendation['advice'].append(f'💡 ウエスト: {waist_range}インチ、股下: {inseam}cm程度がおすすめです')
            
            # 身長別のアドバイス
            if height < 170:
                recommendation['advice'].append('✨ アンクル丈やクロップド丈でバランスを取ると脚長効果があります')
            elif height > 180:
                recommendation['advice'].append('✨ ロング丈を選ぶと身長を活かしたスタイリングができます')
        
        # シューズのサイズ推奨
        elif category == 'shoes':
            # 身長からおおよその足のサイズを推定
            if height < 165:
                shoe_size = '25.0～26.0'
            elif height < 175:
                shoe_size = '26.0～27.0'
            elif height < 185:
                shoe_size = '27.0～28.0'
            else:
                shoe_size = '28.0～29.0'
            
            recommendation['sizes']['recommended'] = f'{shoe_size}cm'
            recommendation['advice'].append(f'💡 目安サイズ: {shoe_size}cm（ブランドによって異なります）')
            recommendation['advice'].append('✨ 必ず試着して、つま先に1cm程度の余裕があるサイズを選びましょう')
        
        return recommendation
    
    def get_style_advice_by_body_type(self) -> Dict:
        """
        体型に合わせたスタイルアドバイスを取得
        
        Returns:
            体型別のスタイルアドバイス
        """
        body_type = self.get_body_type()
        height = self.profile.get('height')
        
        advice = {
            'body_type': body_type,
            'recommended_styles': [],
            'styling_tips': [],
            'items_to_focus': []
        }
        
        if body_type == '痩せ型':
            advice['recommended_styles'] = ['カジュアル', 'ストリート', 'アメカジ']
            advice['styling_tips'] = [
                '🎯 レイヤードスタイルで立体感を出しましょう',
                '🎯 オーバーサイズのアイテムでゆとりを持たせると◎',
                '🎯 ボリュームのあるアウターで存在感アップ'
            ]
            advice['items_to_focus'] = ['厚手のニット', 'オーバーサイズパーカー', 'ボリュームアウター']
        
        elif body_type == '標準':
            advice['recommended_styles'] = ['全てのスタイルOK']
            advice['styling_tips'] = [
                '🎯 バランスの良い体型を活かして、様々なスタイルに挑戦できます',
                '🎯 ジャストサイズでスマートに着こなすのがおすすめ',
                '🎯 トレンドアイテムも積極的に取り入れましょう'
            ]
            advice['items_to_focus'] = ['ジャストサイズのトップス', 'テーパードパンツ', 'きれいめシューズ']
        
        elif body_type in ['ややぽっちゃり', 'ぽっちゃり']:
            advice['recommended_styles'] = ['カジュアル', 'シティ', 'アメカジ']
            advice['styling_tips'] = [
                '🎯 縦のラインを意識したIラインシルエットがおすすめ',
                '🎯 暗めの色で引き締め効果を',
                '🎯 ゆったりめのサイズでリラックス感を出しつつ、体型カバー'
            ]
            advice['items_to_focus'] = ['ロングコート', 'ダークカラーのトップス', 'テーパードパンツ']
        
        # 身長によるアドバイスも追加
        if height:
            if height < 170:
                advice['styling_tips'].append('📏 アンクル丈やクロップド丈で脚長効果を狙いましょう')
            elif height > 180:
                advice['styling_tips'].append('📏 ロング丈のアイテムで身長を活かしたスタイリングを')
        
        return advice
