"""
毎日のファッションコーディネートアプリ
Daily Fashion Coordinator

天気、行き先、スタイルに基づいて最適なコーディネートを提案するStreamlitアプリ
"""
import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# 環境変数を読み込む（.envファイルの絶対パスを指定）
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from weather import WeatherService
from wardrobe import WardrobeManager
from outfit_recommender import OutfitRecommender
from shopping import ShoppingSearcher
from history import OutfitHistoryManager
from export_import import DataExporter, DataImporter
from ai_analyzer import AIClothingAnalyzer
from user_profile import UserProfileManager


# ページ設定
st.set_page_config(
    page_title="✨ FUKU - 毎日のコーデ",
    page_icon="👔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS - スマホ対応＆洗練されたデザイン
st.markdown("""
<style>
    /* Google Fonts - 洗練されたフォント */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans+JP:wght@300;400;500;700;900&display=swap');
    
    /* 全体のフォント設定 */
    * {
        font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        letter-spacing: -0.01em;
    }
    
    /* メインコンテナ */
    .main {
        padding: 0.5rem 1rem;
        max-width: 100%;
    }
    
    /* ヘッダー - グラデーション背景 */
    .main-header {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* セクションヘッダー */
    .section-header {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-size: clamp(1.2rem, 4vw, 1.5rem);
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #2d3748;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 4px solid #667eea;
    }
    
    /* 天気カード - より立体的に */
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: slideInUp 0.6s ease-out;
    }
    
    .weather-card h2 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(2rem, 6vw, 3rem);
        margin: 0.5rem 0;
        font-weight: 700;
        letter-spacing: -0.05em;
    }
    
    .weather-card h3 {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-size: clamp(1.2rem, 4vw, 1.5rem);
        margin-bottom: 0.5rem;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    .weather-card p {
        font-weight: 400;
        letter-spacing: -0.01em;
    }
    
    /* コーデカード */
    .outfit-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid #f0f2f6;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .outfit-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* アイテムカード */
    .item-card {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    
    /* ボタンスタイル */
    .stButton>button {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* タブスタイル */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
    }
    
    /* エクスパンダー */
    .streamlit-expanderHeader {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: -0.01em;
        border-radius: 10px;
    }
    
    /* 画像スタイル */
    img {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* アニメーション */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* スマホ対応 */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .weather-card {
            padding: 1rem;
        }
        
        .outfit-card {
            padding: 1rem;
        }
    }
    
    /* インプットフィールド */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        font-size: 0.95rem;
        font-weight: 400;
        letter-spacing: -0.01em;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* ラベル */
    label {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
        color: #2d3748;
    }
    
    /* 一般的なテキスト */
    p, div, span {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        letter-spacing: -0.01em;
    }
    
    /* h1, h2, h3 */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    
    /* メトリクス */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
    }
    
    /* 成功/エラーメッセージ */
    .stSuccess, .stError, .stWarning, .stInfo {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 500;
        letter-spacing: -0.01em;
        animation: slideInUp 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """セッション状態の初期化"""
    if 'wardrobe_manager' not in st.session_state:
        st.session_state.wardrobe_manager = WardrobeManager()
    if 'weather_service' not in st.session_state:
        st.session_state.weather_service = WeatherService()
    if 'outfit_recommender' not in st.session_state:
        st.session_state.outfit_recommender = OutfitRecommender()
    if 'shopping_searcher' not in st.session_state:
        st.session_state.shopping_searcher = ShoppingSearcher()
    if 'history_manager' not in st.session_state:
        st.session_state.history_manager = OutfitHistoryManager()
    if 'data_exporter' not in st.session_state:
        st.session_state.data_exporter = DataExporter()
    if 'data_importer' not in st.session_state:
        st.session_state.data_importer = DataImporter()
    if 'ai_analyzer' not in st.session_state:
        st.session_state.ai_analyzer = AIClothingAnalyzer()
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = UserProfileManager()


def display_weather_info(weather_data):
    """天気情報を表示 - Streamlit標準コンポーネント版"""
    # 天気による絵文字選択
    weather_emoji = "☀️"
    if "雨" in weather_data['description']:
        weather_emoji = "🌧️"
    elif "曇" in weather_data['description']:
        weather_emoji = "☁️"
    elif "雪" in weather_data['description']:
        weather_emoji = "❄️"
    elif "晴" in weather_data['description']:
        weather_emoji = "☀️"
    
    # 天気情報をコンテナで表示
    with st.container():
        st.markdown(f"### 📍 {weather_data['city']}")
        
        # 気温を大きく表示
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## 🌡️ {weather_data['temperature']}°C")
            st.markdown(f"**体感温度**: {weather_data['feels_like']}°C")
        with col2:
            st.markdown(f"# {weather_emoji}")
        
        # 気温差による警告表示
        temp_diff = abs(weather_data['feels_like'] - weather_data['temperature'])
        if temp_diff > 3:
            if weather_data['feels_like'] < weather_data['temperature']:
                st.warning(f"⚠️ 風で体感温度が{temp_diff:.0f}度低く感じます")
            else:
                st.warning(f"⚠️ 湿度で体感温度が{temp_diff:.0f}度高く感じます")
        
        st.markdown(f"**{weather_data['description']}**")
        
        # 湿度と風速
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💧 湿度", f"{weather_data['humidity']}%")
        with col2:
            st.metric("🌬️ 風速", f"{weather_data['wind_speed']}m/s")


def display_outfit(outfit):
    """コーディネートを表示 - スマホ対応版（気温情報を強調）"""
    st.markdown("## ✨ 今日のコーディネート")
    
    # 気温情報を目立つように表示
    if outfit.get('temperature'):
        temp = outfit['temperature']
        temp_emoji = "🥶" if temp < 5 else "❄️" if temp < 10 else "🍃" if temp < 15 else "😊" if temp < 20 else "🌞" if temp < 25 else "🔥"
        st.info(f"{temp_emoji} **気温 {temp:.0f}°C に最適なコーデ**")
    
    # アイテムごとに縦に並べる（スマホで見やすい）
    outfit_items = [
        ('🧥', 'アウター', outfit['outer']),
        ('👕', 'トップス', outfit['top']),
        ('👖', 'ボトムス', outfit['bottom']),
        ('👟', '靴', outfit['shoes'])
    ]
    
    for emoji, label, item in outfit_items:
        if item:
            st.markdown(f"#### {emoji} {label}")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if item.get('image_path') and os.path.exists(item['image_path']):
                    st.image(item['image_path'], width='stretch')
                else:
                    # 絵文字を大きく表示
                    st.markdown(f"<div style='font-size: 5rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{item['name']}**")
                st.write(f"🎨 {item.get('color', '-')}")
                st.write(f"🏷️ {item.get('brand', '-')}")
    
    # アクセサリー
    if outfit['accessories']:
        st.markdown("#### 🎒 アクセサリー")
        
        cols = st.columns(min(len(outfit['accessories']), 3))
        for idx, acc in enumerate(outfit['accessories']):
            with cols[idx % len(cols)]:
                if acc.get('image_path') and os.path.exists(acc['image_path']):
                    st.image(acc['image_path'], width='stretch')
                st.markdown(f"**{acc['name']}**")
                st.write(f"🎨 {acc.get('color', '-')}")
    
    # 提案理由
    st.markdown("### 💡 このコーデを選んだ理由")
    for idx, reason in enumerate(outfit['reasoning'], 1):
        st.write(f"{idx}. {reason}")
    
    # おしゃれになるワンポイントアドバイス
    if outfit.get('fashion_tip'):
        st.markdown("---")
        st.markdown("### ✨ おしゃれになるワンポイントアドバイス")
        st.success(outfit['fashion_tip'])


def wardrobe_management_page():
    """ワードローブ管理ページ"""
    st.title("👗 ワードローブ管理")
    
    # データ永続化の説明を追加
    st.info("💾 **自動保存機能**：追加したアイテムは自動的に保存されます。ブラウザを閉じても、次回開いたときに復元されます。")
    
    manager = st.session_state.wardrobe_manager
    
    tab1, tab2, tab3 = st.tabs(["📋 アイテム一覧", "➕ アイテム追加", "🔧 管理"])
    
    with tab1:
        st.subheader("現在のワードローブ")
        wardrobe = manager.get_all_items()
        
        for category in ['outer', 'top', 'bottom', 'shoes', 'accessories']:
            category_names = {
                'outer': 'アウター',
                'top': 'トップス',
                'bottom': 'ボトムス',
                'shoes': '靴',
                'accessories': 'アクセサリー'
            }
            
            with st.expander(f"{category_names[category]} ({len(wardrobe[category])}点)", expanded=False):
                items = wardrobe[category]
                if items:
                    # グリッド表示用に3列で配置
                    for i in range(0, len(items), 3):
                        cols = st.columns(3)
                        for j, col in enumerate(cols):
                            if i + j < len(items):
                                item = items[i + j]
                                item_index = i + j  # グリッド内のインデックス
                                with col:
                                    # 画像がある場合は表示
                                    if item.get('image_path') and os.path.exists(item['image_path']):
                                        st.image(item['image_path'], width='stretch')
                                    else:
                                        # 画像がない場合はプレースホルダー
                                        st.markdown(f"""
                                        <div style="background-color: #f0f2f6; 
                                                    padding: 40px; 
                                                    text-align: center; 
                                                    border-radius: 10px;
                                                    margin-bottom: 10px;">
                                            <p style="font-size: 3em; margin: 0;">👕</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    st.write(f"**{item['name']}**")
                                    st.write(f"🎨 {item.get('color', 'N/A')}")
                                    st.write(f"🏷️ {item.get('brand', 'N/A')}")
                                    
                                    # 相性情報を表示
                                    recommender = st.session_state.outfit_recommender
                                    compatibility = recommender.get_item_compatibility(item)
                                    
                                    # 相性の良いスタイル
                                    if compatibility['compatible_styles']:
                                        styles_text = '、'.join(compatibility['compatible_styles'])
                                        st.caption(f"✨ 相性: {styles_text}")
                                    
                                    # 詳細情報をexpanderで表示
                                    with st.expander("💡 組み合わせ提案", key=f"expand_{category}_{item_index}"):
                                        matching = compatibility['matching_items']
                                        
                                        if matching['tops']:
                                            st.write("**👕 合わせやすいトップス:**")
                                            st.write("• " + "、".join(matching['tops']))
                                        
                                        if matching['bottoms']:
                                            st.write("**👖 合わせやすいボトムス:**")
                                            st.write("• " + "、".join(matching['bottoms']))
                                        
                                        if matching['outers']:
                                            st.write("**🧥 合わせやすいアウター:**")
                                            st.write("• " + "、".join(matching['outers']))
                                        
                                        if matching['shoes']:
                                            st.write("**👞 合わせやすい靴:**")
                                            st.write("• " + "、".join(matching['shoes']))
                                        
                                        if matching['tips']:
                                            st.info("\n\n".join(matching['tips']))
                                    
                                    if st.button("🗑️ 削除", key=f"del_{category}_{item_index}_{item.get('id', '')}"):
                                        manager.remove_item(category, item['id'])
                                        st.rerun()
                else:
                    st.write("アイテムがありません")
    
    with tab2:
        st.subheader("新しいアイテムを追加")
        
        # 画像アップロード or テキスト入力の選択
        input_method = st.radio(
            "登録方法を選択",
            ["📸 写真で登録", "✏️ 手動入力"],
            horizontal=True
        )
        
        category = st.selectbox(
            "カテゴリー",
            ['outer', 'top', 'bottom', 'shoes', 'accessories'],
            format_func=lambda x: {
                'outer': 'アウター',
                'top': 'トップス',
                'bottom': 'ボトムス',
                'shoes': '靴',
                'accessories': 'アクセサリー'
            }[x]
        )
        
        uploaded_image = None
        
        if input_method == "📸 写真で登録":
            st.write("### 📸 写真をアップロード")
            uploaded_image = st.file_uploader(
                "服の写真を選択してください",
                type=['png', 'jpg', 'jpeg'],
                help="PNG、JPG、JPEG形式の画像をアップロードできます"
            )
            
            if uploaded_image:
                # 画像プレビュー
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(uploaded_image, caption="プレビュー", width='stretch')
                
                with col2:
                    st.write("### アイテム情報")
                    name = st.text_input("アイテム名", placeholder="例: デニムジャケット", key="img_name")
                    color = st.text_input("色", placeholder="例: ブルー", key="img_color")
                    
                    # ブランド選択（古着オプション + その他自由入力）
                    brand_choice = st.selectbox(
                        "ブランド",
                        ['ユニクロ', 'GU', 'ZARA', 'H&M', '無印良品', 'WEGO', 'ビームス', '古着', 'その他（自分で入力）'],
                        key="img_brand_choice"
                    )
                    
                    # 「その他」を選んだ場合は自由入力
                    if brand_choice == 'その他（自分で入力）':
                        brand = st.text_input("ブランド名を入力", placeholder="例: ナイキ、アディダスなど", key="img_brand_custom")
                    else:
                        brand = brand_choice
        else:
            st.write("### ✏️ 手動で入力")
            name = st.text_input("アイテム名", placeholder="例: デニムジャケット")
            color = st.text_input("色", placeholder="例: ブルー")
            
            # ブランド選択（古着オプション + その他自由入力）
            brand_choice = st.selectbox(
                "ブランド",
                ['ユニクロ', 'GU', 'ZARA', 'H&M', '無印良品', 'WEGO', 'ビームス', '古着', 'その他（自分で入力）'],
                key="manual_brand_choice"
            )
            
            # 「その他」を選んだ場合は自由入力
            if brand_choice == 'その他（自分で入力）':
                brand = st.text_input("ブランド名を入力", placeholder="例: ナイキ、アディダスなど", key="manual_brand_custom")
            else:
                brand = brand_choice
        
        style = st.selectbox(
            "スタイル",
            ['カジュアル', 'ストリート', 'シティ', 'フォーマル', 'アメカジ', 'モード', 'ベーシック']
        )
        season = st.multiselect(
            "適した季節",
            ['春', '夏', '秋', '冬']
        )
        
        if st.button("追加", type="primary"):
            if name:
                item = {
                    'name': name,
                    'color': color,
                    'brand': brand,
                    'style': style,
                    'season': ','.join(season)
                }
                
                # 画像データを取得
                image_data = None
                if uploaded_image:
                    image_data = uploaded_image.read()
                
                if manager.add_item(category, item, image_data):
                    st.success(f"✅ {name}を追加しました！💾 データは自動的に保存されました。")
                    st.rerun()
                else:
                    st.error("❌ 追加に失敗しました")
            else:
                st.warning("アイテム名を入力してください")
    
    with tab3:
        st.subheader("ワードローブ管理")
        
        st.write("### サンプルデータ")
        st.write("サンプルデータをロードして、アプリの機能を試すことができます。")
        
        if st.button("サンプルデータをロード", type="primary"):
            if manager.load_sample_data():
                st.success("サンプルデータをロードしました！")
                st.rerun()
            else:
                st.error("サンプルデータのロードに失敗しました")
        
        st.write("### データの統計")
        wardrobe = manager.get_all_items()
        total_items = sum(len(items) for items in wardrobe.values())
        st.metric("総アイテム数", total_items)


def shopping_page():
    """ショッピングページ"""
    st.title("🛍️ 買い物アドバイス")
    
    st.info("💡 このページでは、あなたのスタイルに必要なアイテムの説明とサイズ感のアドバイスを提供します。")
    
    manager = st.session_state.wardrobe_manager
    profile_manager = st.session_state.user_profile
    
    tab1, tab2 = st.tabs(["🎯 スタイル別アドバイス", "💰 ショッピングのコツ"])
    
    with tab1:
        st.subheader("あなたのスタイルに必要なアイテム")
        
        target_style = st.selectbox(
            "目指したいスタイルを選択",
            ['ストリート', 'シティ', 'カジュアル', 'フォーマル', 'アメカジ', 'モード']
        )
        
        if st.button("アドバイスを見る", type="primary"):
            wardrobe = manager.get_all_items()
            recommender = st.session_state.outfit_recommender
            
            # スタイル別の推奨アイテムを取得
            suggestions = recommender.suggest_additions_for_style(wardrobe, target_style, 20)
            
            if suggestions.get('essential'):
                st.success(f"✨ {target_style}スタイルに必要なアイテムのアドバイス:")
                
                for idx, suggestion in enumerate(suggestions['essential'][:5], 1):
                    with st.expander(f"#{idx} 📦 {suggestion['item']}", expanded=True):
                        st.markdown(f"**💡 なぜ必要？**\n\n{suggestion['reason']}")
                        
                        # サイズ感のアドバイス
                        category = suggestion.get('category', 'top')
                        size_rec = profile_manager.get_size_recommendation(category)
                        
                        if size_rec.get('sizes'):
                            st.markdown("---")
                            st.markdown("### 📏 あなたに合うサイズ感")
                            
                            if 'recommended' in size_rec['sizes']:
                                st.info(f"**おすすめサイズ**: {size_rec['sizes']['recommended']}")
                            elif 'waist' in size_rec['sizes']:
                                st.info(f"**ウエスト**: {size_rec['sizes']['waist']}\n\n**股下**: {size_rec['sizes']['inseam']}")
                            
                            if size_rec.get('advice'):
                                st.markdown("**👔 選び方のコツ:**")
                                for advice in size_rec['advice']:
                                    st.write(f"• {advice}")
                        else:
                            st.warning("📏 プロフィール（身長・体重）を設定すると、サイズアドバイスが表示されます")
                        
                        # 具体的な選び方のアドバイス
                        st.markdown("---")
                        st.markdown("### 🛍️ 選び方のポイント")
                        
                        # アイテム別のアドバイス
                        item_name = suggestion['item'].lower()
                        if 'tシャツ' in item_name or 'カットソー' in item_name:
                            st.write("• **素材**: コットン100%が快適（夏は吸汗速乾素材もおすすめ）")
                            st.write("• **フィット**: 肩幅がぴったり合うものを選ぶ")
                            st.write("• **丈**: ベルトより5cm程度長いのが理想")
                        elif 'パンツ' in item_name or 'デニム' in item_name or 'ジーンズ' in item_name:
                            st.write("• **ウエスト**: 指1本分の余裕があるサイズ")
                            st.write("• **股下**: 靴を履いて少し裾が地面に触れる長さ")
                            st.write("• **シルエット**: スリムかストレートが合わせやすい")
                        elif 'ジャケット' in item_name or 'アウター' in item_name:
                            st.write("• **肩**: 肩のラインが自然に合うものを選ぶ")
                            st.write("• **袖丈**: 手首の骨が見える程度")
                            st.write("• **着丈**: ヒップが隠れる程度が基本")
                        elif 'シューズ' in item_name or '靴' in item_name:
                            st.write("• **サイズ**: つま先に1cm程度の余裕")
                            st.write("• **試着**: 必ず両足で歩いてみる")
                            st.write("• **時間帯**: 午後に試着するのがベスト（足がむくむため）")
                        
                        # 購入場所のヒント（リンクなし）
                        st.markdown("---")
                        st.markdown("### 🏪 どこで買う？")
                        st.write("**おすすめの購入場所:**")
                        st.write("• ユニクロ・GU: ベーシックアイテムがお手頃")
                        st.write("• ZARA・H&M: トレンド感のあるアイテム")
                        st.write("• 無印良品: シンプルで品質が良い")
                        st.write("• WEGO: ストリート系なら")
            else:
                st.info(f"✨ {target_style}スタイルに必要な基本アイテムは揃っています！")
        
    with tab2:
        st.subheader("💰 お手頃ショッピングのコツ")
        
        tips = [
            "🏷️ **セール時期を狙う**: 春夏物は7月、秋冬物は1月が狙い目",
            "📱 **アプリクーポン**: 各ブランドの公式アプリでクーポンゲット",
            "🔄 **定番アイテムから**: 流行に左右されない基本アイテムを優先",
            "👕 **試着は必須**: サイズ感を確認してから購入",
            "💳 **予算を決める**: 1着あたりの予算を決めて計画的に",
            "🎯 **必要なものリスト**: 衝動買いを避けるためリストを作る"
        ]
        
        for tip in tips:
            st.write(tip)
        
        st.write("---")
        st.subheader("💵 各ブランドの価格帯目安")
        
        price_info = {
            "ユニクロ・GU": "1,000〜5,000円（ベーシックで高コスパ）",
            "ZARA・H&M": "2,000〜8,000円（トレンド重視）",
            "無印良品": "2,000〜10,000円（シンプル・高品質）",
            "WEGO": "1,500〜5,000円（ストリート系）",
            "ビームス・ユナイテッドアローズ": "5,000〜20,000円（セレクトショップ）"
        }
        
        for brand, price in price_info.items():
            st.write(f"**{brand}**")
            st.write(f"　{price}")
            st.write("")


def favorite_item_outfit_page():
    """お気に入りアイテムからコーディネートを組むページ"""
    st.title("💖 お気に入りアイテムからコーデを組む")
    
    st.info("✨ 絶対に使いたいアイテムを選んで、それに合うコーディネートを提案します。")
    
    manager = st.session_state.wardrobe_manager
    recommender = st.session_state.outfit_recommender
    wardrobe = manager.get_all_items()
    
    # 全アイテム数を確認
    total_items = sum(len(items) for items in wardrobe.values())
    
    if total_items == 0:
        st.warning("⚠️ ワードローブが空です。左メニューの「ワードローブ管理」からアイテムを追加してください。")
        return
    
    # カテゴリー選択
    st.subheader("1️⃣ ベースにするアイテムのカテゴリーを選択")
    category = st.selectbox(
        "カテゴリー",
        ['outer', 'top', 'bottom', 'shoes', 'accessories'],
        format_func=lambda x: {
            'outer': '🧥 アウター',
            'top': '👕 トップス',
            'bottom': '👖 ボトムス',
            'shoes': '👟 靴',
            'accessories': '🎒 アクセサリー'
        }[x],
        key="favorite_category"
    )
    
    # そのカテゴリーのアイテム一覧を表示
    items = wardrobe[category]
    
    if not items:
        st.warning(f"このカテゴリーにアイテムがありません。先にアイテムを追加してください。")
        return
    
    st.subheader("2️⃣ 使いたいアイテムを選択")
    
    # アイテムを選択しやすいように表示
    item_options = {}
    for item in items:
        item_key = f"{item['name']} - {item.get('color', 'N/A')} ({item.get('brand', 'N/A')})"
        item_options[item_key] = item
    
    selected_item_key = st.selectbox(
        "アイテムを選択",
        list(item_options.keys()),
        key="favorite_item_select"
    )
    
    selected_item = item_options[selected_item_key]
    
    # 選択したアイテムを表示
    st.markdown("### 選択したアイテム")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if selected_item.get('image_path') and os.path.exists(selected_item['image_path']):
            st.image(selected_item['image_path'], width='stretch')
        else:
            # カテゴリーに応じた絵文字を表示
            emoji_map = {
                'outer': '🧥',
                'top': '👕',
                'bottom': '👖',
                'shoes': '👟',
                'accessories': '🎒'
            }
            st.markdown(f"<div style='font-size: 5rem; text-align: center;'>{emoji_map.get(category, '👔')}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**名前**: {selected_item['name']}")
        st.markdown(f"**色**: {selected_item.get('color', 'N/A')}")
        st.markdown(f"**ブランド**: {selected_item.get('brand', 'N/A')}")
        st.markdown(f"**スタイル**: {selected_item.get('style', 'N/A')}")
    
    # 天気情報を取得
    with st.sidebar:
        st.header("⚙️ コーディネート設定")
        
        st.subheader("📍 場所")
        city = st.text_input("都市名", value=st.session_state.get('last_city', 'Tokyo'))
        st.session_state.last_city = city
        
        st.subheader("🎯 今日の予定")
        destination = st.selectbox(
            "行き先",
            ['大学', '仕事・オフィス', 'デート', 'カフェ・友達と', 
             'ショッピング', 'アウトドア', 'パーティー'],
            key="fav_destination"
        )
    
    st.markdown("---")
    
    # コーディネート生成ボタン
    if st.button("🎨 このアイテムでコーディネート生成", type="primary"):
        weather_service = st.session_state.weather_service
        weather_data = weather_service.get_weather(city)
        
        if not weather_data:
            st.error("天気情報の取得に失敗しました")
            return
        
        # 天気に基づく推奨を取得
        weather_rec = weather_service.get_clothing_recommendation(weather_data)
        effective_temp = weather_rec.get('feels_like_temp', weather_data['feels_like'])
        
        # 選択したアイテムをベースにコーディネートを生成
        outfit = recommender.recommend_outfit_from_item(
            wardrobe,
            selected_item,
            category,
            weather_rec,
            destination,
            effective_temp
        )
        
        # 天気情報を表示
        st.markdown("### 🌤️ 今日の天気")
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            st.metric("🌡️ 気温", f"{weather_data['temperature']}°C")
        with col_w2:
            st.metric("💧 湿度", f"{weather_data['humidity']}%")
        with col_w3:
            st.metric("🌬️ 風速", f"{weather_data['wind_speed']}m/s")
        
        st.markdown(f"**{weather_data['description']}**")
        
        st.markdown("---")
        
        # コーディネートを表示
        st.markdown("## ✨ 提案コーディネート")
        
        # 気温情報を目立つように表示
        temp_emoji = "🥶" if effective_temp < 5 else "❄️" if effective_temp < 10 else "🍃" if effective_temp < 15 else "😊" if effective_temp < 20 else "🌞" if effective_temp < 25 else "🔥"
        st.info(f"{temp_emoji} **気温 {effective_temp:.0f}°C に最適なコーデ**")
        
        # アイテムごとに縦に並べる
        outfit_items = [
            ('🧥', 'アウター', outfit.get('outer'), 'outer'),
            ('👕', 'トップス', outfit.get('top'), 'top'),
            ('👖', 'ボトムス', outfit.get('bottom'), 'bottom'),
            ('👟', '靴', outfit.get('shoes'), 'shoes')
        ]
        
        for emoji, label, item, cat in outfit_items:
            if item:
                # 選択したアイテムを強調表示
                is_selected = (cat == category and item.get('id') == selected_item.get('id'))
                
                if is_selected:
                    st.markdown(f"#### {emoji} {label} 💖 **（あなたの選んだアイテム）**")
                else:
                    st.markdown(f"#### {emoji} {label}")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    if item.get('image_path') and os.path.exists(item['image_path']):
                        st.image(item['image_path'], width='stretch')
                    else:
                        st.markdown(f"<div style='font-size: 5rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{item['name']}**")
                    st.write(f"🎨 {item.get('color', '-')}")
                    st.write(f"🏷️ {item.get('brand', '-')}")
                    
                    if is_selected:
                        st.success("💖 これがベースです！")
        
        # アクセサリー
        if outfit.get('accessories'):
            st.markdown("#### 🎒 アクセサリー")
            
            cols = st.columns(min(len(outfit['accessories']), 3))
            for idx, acc in enumerate(outfit['accessories']):
                with cols[idx % len(cols)]:
                    if acc.get('image_path') and os.path.exists(acc['image_path']):
                        st.image(acc['image_path'], width='stretch')
                    st.markdown(f"**{acc['name']}**")
                    st.write(f"🎨 {acc.get('color', '-')}")
        
        # 提案理由
        st.markdown("### 💡 このコーデを選んだ理由")
        for idx, reason in enumerate(outfit.get('reasoning', []), 1):
            st.write(f"{idx}. {reason}")
        
        # 組み合わせのコツ
        if outfit.get('styling_tips'):
            st.markdown("### 👔 スタイリングのコツ")
            for tip in outfit['styling_tips']:
                st.info(tip)
        
        # おしゃれになるワンポイントアドバイス
        if outfit.get('fashion_tip'):
            st.markdown("---")
            st.markdown("### ✨ おしゃれになるワンポイントアドバイス")
            st.success(outfit['fashion_tip'])


def main_page():
    """メインページ - コーディネート提案"""
    # 楽しいヘッダー
    greetings = ["✨", "🌟", "💫", "⭐", "🎉", "🎊"]
    import random
    emoji = random.choice(greetings)
    
    st.title(f"{emoji} FUKU - 今日のコーデ {emoji}")
    
    # データ永続化の状態を表示
    manager = st.session_state.wardrobe_manager
    wardrobe = manager.get_all_items()
    total_items = sum(len(items) for items in wardrobe.values())
    if total_items > 0:
        st.success(f"💾 {total_items}点のアイテムが保存されています（自動保存済み）")
    
    # 日付表示を可愛く
    weekday_jp = {'Monday': '月', 'Tuesday': '火', 'Wednesday': '水', 
                  'Thursday': '木', 'Friday': '金', 'Saturday': '土', 'Sunday': '日'}
    today = datetime.now()
    weekday = weekday_jp.get(today.strftime('%A'), '')
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0; padding: 1rem; 
                background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 15px;">
        <h3 style="margin: 0; color: #495057;">📅 {today.strftime('%Y年%m月%d日')} ({weekday})</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # サイドバー設定
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # APIキーの状態を表示
        weather_service = st.session_state.weather_service
        api_key = weather_service.api_key
        
        # デバッグ情報を表示
        st.write(f"🔑 APIキー: {api_key[:10]}..." if api_key and len(api_key) > 10 else f"🔑 APIキー: {api_key}")
        
        if api_key and api_key != 'your_api_key_here':
            st.success("🌐 リアルタイム天気情報: 有効")
        else:
            st.info("📊 デモモード（固定気温20度）")
            with st.expander("💡 リアルタイム天気情報を使うには"):
                st.write("""
                1. [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)でアカウント作成
                2. [APIキー](https://home.openweathermap.org/api_keys)を取得
                3. `.env`ファイルに設定
                4. アプリを再起動
                """)
        
        st.markdown("---")
        st.subheader("📍 場所")
        
        # 日本の都市データをインポート
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
            from japan_cities import get_all_prefectures, get_cities_by_prefecture
            
            # 都道府県と都市の選択
            selection_method = st.radio(
                "選択方法",
                ["🗾 都道府県から選択", "✏️ 直接入力"],
                horizontal=True
            )
            
            if selection_method == "🗾 都道府県から選択":
                col_pref, col_city = st.columns(2)
                
                with col_pref:
                    prefecture = st.selectbox(
                        "都道府県",
                        get_all_prefectures(),
                        index=get_all_prefectures().index(st.session_state.get('last_prefecture', '東京都'))
                    )
                    st.session_state.last_prefecture = prefecture
                
                with col_city:
                    cities = get_cities_by_prefecture(prefecture)
                    if cities:
                        city_options = list(cities.keys())
                        selected_jp_city = st.selectbox(
                            "都市",
                            city_options,
                            index=0
                        )
                        city = cities[selected_jp_city]
                        st.session_state.last_city = city
                    else:
                        city = 'Tokyo'
            
            else:
                # 直接入力
                city = st.text_input(
                    "都市名を入力",
                    value=st.session_state.get('last_city', 'Tokyo'),
                    help="日本語または英語で都市名を入力",
                    placeholder="例: 渋谷区、Fukuoka"
                )
                st.session_state.last_city = city
        
        except ImportError:
            # フォールバック
            city = st.text_input("都市名", value="Tokyo")
            st.session_state.last_city = city
        
        # ユーザープロフィール設定
        with st.expander("👤 プロフィール設定"):
            profile_manager = st.session_state.user_profile
            current_profile = profile_manager.get_profile()
            
            col_h, col_w = st.columns(2)
            with col_h:
                height = st.number_input(
                    "身長 (cm)",
                    min_value=140,
                    max_value=200,
                    value=current_profile.get('height') or 170,
                    step=1
                )
            with col_w:
                weight = st.number_input(
                    "体重 (kg)",
                    min_value=40,
                    max_value=120,
                    value=current_profile.get('weight') or 60,
                    step=1
                )
            
            preferred_fit = st.selectbox(
                "好みのフィット感",
                ['regular', 'oversized'],
                format_func=lambda x: 'ジャストサイズ' if x == 'regular' else 'オーバーサイズ',
                index=0 if current_profile.get('preferred_fit') == 'regular' else 1
            )
            
            if st.button("プロフィールを更新"):
                if profile_manager.update_profile(height=height, weight=weight, preferred_fit=preferred_fit):
                    st.success("✅ プロフィールを更新しました")
                    # BMIと体型を表示
                    bmi = profile_manager.calculate_bmi()
                    body_type = profile_manager.get_body_type()
                    st.info(f"📊 BMI: {bmi} / 体型: {body_type}")
                else:
                    st.error("更新に失敗しました")
        
        st.subheader("🎯 今日の予定")
        destination = st.selectbox(
            "行き先",
            ['大学', '仕事・オフィス', 'デート', 'カフェ・友達と', 
             'ショッピング', 'アウトドア', 'パーティー']
        )
        
        st.subheader("👕 好みのスタイル")
        preferred_style = st.selectbox(
            "スタイル",
            ['カジュアル', 'ストリート', 'シティ', 'フォーマル', 'アメカジ', 'モード']
        )
        
        # スタイルの詳細説明（エラーハンドリング付き）
        try:
            recommender = st.session_state.outfit_recommender
            style_info = recommender.get_style_description(preferred_style)
            if style_info:
                with st.expander(f"ℹ️ {preferred_style}スタイルの詳細を見る", expanded=False):
                    # スタイル画像を表示（エラーでもスキップして続行）
                    if style_info.get('image_url'):
                        try:
                            st.image(style_info['image_url'], width='stretch')
                        except Exception:
                            pass
                    # 説明文を表示
                    if style_info.get('description'):
                        st.markdown(style_info['description'])
        except Exception:
            # スタイル情報の取得に失敗してもアプリは続行
            pass
        
        generate_button = st.button("🎨 コーディネート生成", type="primary")
    
    # メインコンテンツ
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🌤️ 今日の天気")
        weather_service = st.session_state.weather_service
        weather_data = weather_service.get_weather(city)
        
        if weather_data:
            display_weather_info(weather_data)
        else:
            st.error("天気情報の取得に失敗しました")
    
    with col2:
        if generate_button or 'current_outfit' in st.session_state:
            manager = st.session_state.wardrobe_manager
            recommender = st.session_state.outfit_recommender
            
            # ワードローブが空の場合、サンプルデータを促す
            wardrobe = manager.get_all_items()
            total_items = sum(len(items) for items in wardrobe.values())
            
            if total_items == 0:
                st.warning("⚠️ ワードローブが空です。左メニューの「ワードローブ管理」からアイテムを追加するか、サンプルデータをロードしてください。")
            else:
                # 天気に基づく推奨を取得
                weather_rec = weather_service.get_clothing_recommendation(weather_data)
                
                # 体感温度を取得
                effective_temp = weather_rec.get('feels_like_temp', weather_data['feels_like'])
                
                # コーディネートを生成
                outfit = recommender.recommend_outfit(
                    wardrobe,
                    weather_rec,
                    destination,
                    preferred_style,
                    effective_temp
                )
                
                st.session_state.current_outfit = outfit
                st.session_state.current_weather = weather_data
                st.session_state.current_destination = destination
                st.session_state.current_style = preferred_style
                
                # 履歴に保存（新規生成時のみ）
                if generate_button:
                    history_manager = st.session_state.history_manager
                    history_manager.add_outfit(
                        outfit, 
                        weather_data, 
                        destination, 
                        preferred_style
                    )
                
                # コーディネートを表示
                display_outfit(outfit)
                
                # インスピレーションリンク
                st.markdown("### ✨ インスピレーション")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    pinterest_url = recommender.generate_pinterest_search_url(outfit, preferred_style)
                    st.markdown(f"### 📌 Pinterest")
                    st.markdown(f"[Pinterestで{preferred_style}コーデを見る]({pinterest_url})")
                    st.write("似たようなコーディネートのアイデアを探せます")
                
                with col_b:
                    instagram_url = recommender.generate_instagram_search_url(preferred_style)
                    st.markdown(f"### 📸 Instagram")
                    st.markdown(f"[Instagramで#{preferred_style}コーデを見る]({instagram_url})")
                    st.write("最新のトレンドコーデをチェック")
                
                # ワードローブ分析と提案
                st.markdown("---")
                st.markdown("### 💡 あなたへのおすすめ")
                
                # プロフィール情報を取得
                profile_manager = st.session_state.user_profile
                profile = profile_manager.get_profile()
                
                # サイズアドバイスを表示
                if profile.get('height') and profile.get('weight'):
                    body_type = profile_manager.get_body_type()
                    bmi = profile_manager.calculate_bmi()
                    
                    st.info(f"👤 あなたのプロフィール: 身長 {profile['height']}cm / 体重 {profile['weight']}kg / 体型: {body_type} (BMI: {bmi})")
                    
                    # 体型別のスタイルアドバイス
                    style_advice = profile_manager.get_style_advice_by_body_type()
                    with st.expander("📐 あなたの体型に合わせたアドバイス"):
                        st.markdown("**おすすめのスタイル:**")
                        for style in style_advice['recommended_styles']:
                            st.write(f"• {style}")
                        
                        st.markdown("**スタイリングのコツ:**")
                        for tip in style_advice['styling_tips']:
                            st.write(tip)
                        
                        st.markdown("**注目アイテム:**")
                        for item in style_advice['items_to_focus']:
                            st.write(f"• {item}")
                else:
                    st.warning("👤 プロフィール（身長・体重）を設定すると、あなたに最適なサイズアドバイスが表示されます")
                
                # 汎用性の高いアイテムの提案
                wardrobe = manager.get_all_items()
                versatility_analysis = recommender.analyze_wardrobe_versatility(wardrobe)
                
                # 買い足すべきアイテムの提案
                suggestions = recommender.suggest_additions_for_style(
                    wardrobe, 
                    preferred_style,
                    weather_data['temperature']
                )
                
                col_x, col_y = st.columns(2)
                
                with col_x:
                    st.markdown("#### 🎯 買い足すと便利なアイテム")
                    if suggestions['essential']:
                        for sug in suggestions['essential'][:3]:  # 最大3つ表示
                            # カテゴリーからサイズ推奨を取得
                            category = sug.get('category', 'top')
                            size_rec = profile_manager.get_size_recommendation(category)
                            
                            item_info = f"**{sug['item']}**\n\n{sug['reason']}"
                            
                            # サイズ情報を追加
                            if profile.get('height') and profile.get('weight'):
                                if 'recommended' in size_rec.get('sizes', {}):
                                    item_info += f"\n\n📏 **おすすめサイズ**: {size_rec['sizes']['recommended']}"
                                elif 'waist' in size_rec.get('sizes', {}):
                                    item_info += f"\n\n📏 **サイズ目安**: {size_rec['sizes']['waist']}"
                            
                            st.info(item_info)
                    elif versatility_analysis['missing_basics']:
                        for basic in versatility_analysis['missing_basics'][:3]:
                            # カテゴリーからサイズ推奨を取得
                            category = basic.get('category', 'top')
                            size_rec = profile_manager.get_size_recommendation(category)
                            
                            item_info = f"**{basic['item']}**\n\n{basic['reason']}"
                            
                            # サイズ情報を追加
                            if profile.get('height') and profile.get('weight'):
                                if 'recommended' in size_rec.get('sizes', {}):
                                    item_info += f"\n\n📏 **おすすめサイズ**: {size_rec['sizes']['recommended']}"
                            
                            st.info(item_info)
                    else:
                        st.success("✨ 基本アイテムが揃っています！")
                
                with col_y:
                    st.markdown("#### ⭐ あなたの万能アイテム")
                    if versatility_analysis['versatile_items']:
                        for v_item in versatility_analysis['versatile_items'][:3]:
                            item = v_item['item']
                            st.success(f"**{item['name']}**\n\n汎用性スコア: {v_item['score']}/10")
                    else:
                        st.info("アイテムを追加すると、汎用性分析が表示されます")
                
                # コーディネートイメージの生成
                if suggestions['essential'] or versatility_analysis['missing_basics']:
                    st.markdown("---")
                    st.markdown("### 👔 このコーディネートを見る")
                    st.write("提案したアイテムを組み合わせた実際のコーディネートイメージを確認できます")
                    
                    # 提案アイテムを取得
                    items_to_show = suggestions['essential'][:3] if suggestions['essential'] else versatility_analysis['missing_basics'][:3]
                    
                    # プロンプトを生成
                    current_temp = 20  # デフォルト値
                    if 'current_weather' in st.session_state and st.session_state.current_weather:
                        current_temp = st.session_state.current_weather.get('temperature', 20)
                    
                    prompt = recommender.generate_outfit_preview_prompt(
                        items_to_show,
                        wardrobe,
                        preferred_style,
                        current_temp
                    )
                    
                    # 組み合わせの詳細を表示
                    combination = recommender.create_outfit_combination(
                        items_to_show,
                        wardrobe,
                        preferred_style
                    )
                    
                    st.info(f"✨ {combination['description']}")
                    
                    # コーディネートの詳細
                    with st.expander("📋 コーディネートの詳細", expanded=True):
                        col_new, col_existing = st.columns(2)
                        
                        with col_new:
                            st.markdown("**🆕 新しく買うアイテム:**")
                            for new_item in combination['new_items']:
                                st.write(f"• {new_item['name']}")
                                st.caption(new_item.get('reason', ''))
                        
                        with col_existing:
                            st.markdown("**👔 手持ちのアイテム:**")
                            if combination['existing_items']:
                                for existing_item in combination['existing_items']:
                                    color = existing_item.get('color', '')
                                    name = existing_item['name']
                                    st.write(f"• {color} {name}" if color else f"• {name}")
                            else:
                                st.write("（提案アイテムで完成します）")
                        
                        # スタイリングのコツ
                        st.markdown("**💡 スタイリングのコツ:**")
                        for tip in combination['styling_tips']:
                            st.write(tip)
                    
                    # 色味とアイテムの使い方アドバイス
                    st.markdown("---")
                    st.markdown("### 🎨 おすすめの色味と使い方")
                    
                    # スタイル別の色味アドバイス
                    color_advice = {
                        'カジュアル': {
                            'colors': ['ネイビー', 'ベージュ', 'グレー', 'ホワイト', 'デニムブルー'],
                            'tip': '**ベーシックカラー**を中心に揃えると、どんな組み合わせでも失敗しません。'
                        },
                        'ストリート': {
                            'colors': ['ブラック', 'ホワイト', 'グレー', 'カーキ', 'ワインレッド'],
                            'tip': '**モノトーン**をベースに、差し色で個性を出すのがポイント。'
                        },
                        'シティ': {
                            'colors': ['ネイビー', 'グレー', 'ブラック', 'ホワイト', 'ライトブルー'],
                            'tip': '**落ち着いたトーン**で統一すると、洗練された印象になります。'
                        },
                        'フォーマル': {
                            'colors': ['ネイビー', 'チャコールグレー', 'ブラック', 'ホワイト', 'ライトブルー'],
                            'tip': '**ダークトーン**のスーツに、明るめのシャツで清潔感を。'
                        },
                        'アメカジ': {
                            'colors': ['デニムブルー', 'ブラウン', 'カーキ', 'ホワイト', 'グレー'],
                            'tip': '**アースカラー**で統一すると、ヴィンテージ感が出ます。'
                        },
                        'モード': {
                            'colors': ['ブラック', 'ホワイト', 'グレー', 'ダークネイビー'],
                            'tip': '**モノトーン**のみで構成するのが基本。シルエットで魅せる。'
                        }
                    }
                    
                    advice = color_advice.get(preferred_style, color_advice['カジュアル'])
                    
                    st.markdown(f"**{preferred_style}スタイルにおすすめの色:**")
                    cols = st.columns(len(advice['colors']))
                    for idx, color in enumerate(advice['colors']):
                        with cols[idx]:
                            st.markdown(f"**{color}**")
                    
                    st.info(f"💡 {advice['tip']}")
                    
                    # 汎用性の高いアイテムと色の組み合わせ
                    st.markdown("#### 🌟 一番使える色味の組み合わせ")
                    
                    versatile_combos = [
                        {
                            'top': 'ホワイトのTシャツ',
                            'bottom': 'ネイビーのパンツ',
                            'reason': 'どんなアウターにも合う最強の組み合わせ'
                        },
                        {
                            'top': 'グレーのスウェット',
                            'bottom': 'ブラックのパンツ',
                            'reason': 'カジュアルにもきれいめにも使える万能コンビ'
                        },
                        {
                            'top': 'ネイビーのシャツ',
                            'bottom': 'ベージュのチノパン',
                            'reason': 'きれいめスタイルの定番。デートにも最適'
                        }
                    ]
                    
                    for combo in versatile_combos:
                        st.write(f"• **{combo['top']} × {combo['bottom']}**")
                        st.caption(f"  → {combo['reason']}")
                    
                    # 買い足すべき優先順位
                    st.markdown("---")
                    st.markdown("#### 📊 買い足す優先順位")
                    
                    priority_items = [
                        {'item': '白のTシャツ（無地）', 'reason': 'すべてのスタイルの土台。3枚は欲しい', 'priority': '最優先'},
                        {'item': 'ネイビーorブラックのパンツ', 'reason': 'どんなトップスとも相性抜群', 'priority': '最優先'},
                        {'item': 'グレーのパーカー', 'reason': 'カジュアルの定番。重ね着にも使える', 'priority': '高'},
                        {'item': 'ベージュのチノパン', 'reason': 'きれいめにもカジュアルにも使える', 'priority': '高'},
                        {'item': 'デニムジャケット', 'reason': '春秋の万能アウター', 'priority': '中'}
                    ]
                    
                    for item_info in priority_items:
                        priority_emoji = '🔴' if item_info['priority'] == '最優先' else '🟠' if item_info['priority'] == '高' else '🟡'
                        st.write(f"{priority_emoji} **{item_info['item']}** ({item_info['priority']})")
                        st.caption(f"  {item_info['reason']}")
        else:
            st.info("👈 左側の設定を確認して、「コーディネート生成」ボタンを押してください")


def history_page():
    """履歴ページ"""
    st.title("📊 コーディネート履歴")
    
    history_manager = st.session_state.history_manager
    
    tab1, tab2, tab3 = st.tabs(["📋 履歴一覧", "📈 統計", "⭐ お気に入り"])
    
    with tab1:
        st.subheader("過去のコーディネート")
        
        history = history_manager.get_history(limit=20)
        
        if not history:
            st.info("まだコーディネートの履歴がありません。ホームで コーディネートを生成してください。")
        else:
            for entry in history:
                with st.expander(
                    f"📅 {datetime.fromisoformat(entry['date']).strftime('%Y/%m/%d %H:%M')} - "
                    f"{entry['style']} / {entry['destination']}", 
                    expanded=False
                ):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("### コーディネート")
                        outfit = entry['outfit']
                        
                        if outfit.get('outer'):
                            st.write(f"🧥 **アウター**: {outfit['outer']['name']}")
                        if outfit.get('top'):
                            st.write(f"👕 **トップス**: {outfit['top']['name']}")
                        if outfit.get('bottom'):
                            st.write(f"👖 **ボトムス**: {outfit['bottom']['name']}")
                        if outfit.get('shoes'):
                            st.write(f"👟 **靴**: {outfit['shoes']['name']}")
                    
                    with col2:
                        st.write("### 天気")
                        weather = entry['weather']
                        st.write(f"🌡️ {weather['temperature']}°C")
                        st.write(f"☁️ {weather['description']}")
                        
                        st.write("### 評価")
                        rating = st.select_slider(
                            "満足度",
                            options=[0, 1, 2, 3, 4, 5],
                            value=entry.get('rating', 0),
                            key=f"rating_{entry['id']}"
                        )
                        
                        if rating != entry.get('rating', 0):
                            if history_manager.update_rating(entry['id'], rating):
                                st.success("評価を更新しました！")
                                st.rerun()
                    
                    st.write("### メモ")
                    notes = st.text_area(
                        "メモを追加",
                        value=entry.get('notes', ''),
                        key=f"notes_{entry['id']}",
                        height=100
                    )
                    
                    col_a, col_b = st.columns([1, 5])
                    with col_a:
                        if st.button("💾 保存", key=f"save_{entry['id']}"):
                            if history_manager.update_notes(entry['id'], notes):
                                st.success("メモを保存しました！")
                                st.rerun()
                    
                    with col_b:
                        if st.button("🗑️ 削除", key=f"delete_{entry['id']}"):
                            if history_manager.delete_outfit(entry['id']):
                                st.success("履歴を削除しました")
                                st.rerun()
    
    with tab2:
        st.subheader("統計情報")
        
        stats = history_manager.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("総コーデ数", stats['total_outfits'])
        
        with col2:
            st.metric("平均評価", f"{stats['average_rating']}/5")
        
        with col3:
            st.metric("最多スタイル", stats['most_used_style'] or "N/A")
        
        with col4:
            st.metric("最多行き先", stats['most_common_destination'] or "N/A")
        
        if stats['total_outfits'] > 0:
            st.write("---")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.write("### スタイル分布")
                if stats.get('style_distribution'):
                    for style, count in sorted(
                        stats['style_distribution'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    ):
                        percentage = (count / stats['total_outfits']) * 100
                        st.write(f"**{style}**: {count}回 ({percentage:.1f}%)")
            
            with col_b:
                st.write("### 行き先分布")
                if stats.get('destination_distribution'):
                    for dest, count in sorted(
                        stats['destination_distribution'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    ):
                        percentage = (count / stats['total_outfits']) * 100
                        st.write(f"**{dest}**: {count}回 ({percentage:.1f}%)")
    
    with tab3:
        st.subheader("お気に入りコーディネート")
        
        favorites = history_manager.get_favorite_outfits(min_rating=4)
        
        if not favorites:
            st.info("評価4以上のコーディネートがまだありません")
        else:
            st.write(f"**{len(favorites)}個のお気に入り**")
            
            for entry in favorites:
                with st.expander(
                    f"⭐ {entry['rating']}/5 - "
                    f"{datetime.fromisoformat(entry['date']).strftime('%Y/%m/%d')} - "
                    f"{entry['style']}",
                    expanded=False
                ):
                    outfit = entry['outfit']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if outfit.get('outer'):
                            st.write(f"🧥 {outfit['outer']['name']}")
                        if outfit.get('top'):
                            st.write(f"👕 {outfit['top']['name']}")
                        if outfit.get('bottom'):
                            st.write(f"👖 {outfit['bottom']['name']}")
                        if outfit.get('shoes'):
                            st.write(f"👟 {outfit['shoes']['name']}")
                    
                    with col2:
                        st.write(f"**天気**: {entry['weather']['temperature']}°C")
                        st.write(f"**行き先**: {entry['destination']}")
                        
                        if entry.get('notes'):
                            st.write(f"**メモ**: {entry['notes']}")


def data_management_page():
    """データ管理ページ"""
    st.title("💾 データ管理")
    
    manager = st.session_state.wardrobe_manager
    history_manager = st.session_state.history_manager
    exporter = st.session_state.data_exporter
    importer = st.session_state.data_importer
    
    tab1, tab2 = st.tabs(["📤 エクスポート", "📥 インポート"])
    
    with tab1:
        st.subheader("データのエクスポート")
        
        st.write("ワードローブと履歴をバックアップできます。")
        
        wardrobe = manager.get_all_items()
        history = history_manager.get_history()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("ワードローブアイテム数", sum(len(items) for items in wardrobe.values()))
        
        with col2:
            st.metric("コーディネート履歴数", len(history))
        
        st.write("---")
        
        # JSONエクスポート
        st.write("### JSON形式でエクスポート")
        
        if st.button("📄 JSONをダウンロード", type="primary"):
            json_data = exporter.export_to_json(wardrobe, history)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            st.download_button(
                label="💾 ダウンロード",
                data=json_data,
                file_name=f"fashion_backup_{timestamp}.json",
                mime="application/json"
            )
        
        st.write("---")
        
        # ZIPエクスポート
        st.write("### ZIP形式でエクスポート")
        st.write("ワードローブと履歴を別々のファイルとしてZIPに圧縮します。")
        
        if st.button("📦 ZIPをダウンロード", type="primary"):
            zip_data = exporter.create_backup_zip(wardrobe, history)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            st.download_button(
                label="💾 ダウンロード",
                data=zip_data,
                file_name=f"fashion_backup_{timestamp}.zip",
                mime="application/zip"
            )
    
    with tab2:
        st.subheader("データのインポート")
        
        st.warning("⚠️ インポートすると現在のデータが上書きされます。事前にバックアップを取ることをおすすめします。")
        
        st.write("### JSONファイルからインポート")
        
        uploaded_file = st.file_uploader(
            "JSONファイルを選択",
            type=['json'],
            help="エクスポートしたJSONファイルをアップロード"
        )
        
        if uploaded_file is not None:
            try:
                json_string = uploaded_file.read().decode('utf-8')
                result = importer.import_from_json(json_string)
                
                if result['success']:
                    st.success("✅ データの読み込みに成功しました")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        wardrobe_items = sum(
                            len(items) for items in result['wardrobe'].values()
                        )
                        st.metric("ワードローブアイテム", wardrobe_items)
                    
                    with col2:
                        st.metric("コーディネート履歴", len(result['history']))
                    
                    if st.button("📥 このデータをインポートする", type="primary"):
                        # ワードローブを更新
                        manager.wardrobe = result['wardrobe']
                        manager._save_wardrobe()
                        
                        # 履歴を更新
                        history_manager.history = result['history']
                        history_manager._save_history()
                        
                        st.success("✅ データをインポートしました！")
                        st.rerun()
                
                else:
                    st.error(f"❌ エラー: {result['error']}")
            
            except Exception as e:
                st.error(f"❌ ファイルの読み込みに失敗しました: {str(e)}")
        
        st.write("---")
        
        st.write("### ZIPファイルからインポート")
        
        uploaded_zip = st.file_uploader(
            "ZIPファイルを選択",
            type=['zip'],
            help="エクスポートしたZIPファイルをアップロード"
        )
        
        if uploaded_zip is not None:
            try:
                zip_data = uploaded_zip.read()
                result = importer.import_from_zip(zip_data)
                
                if result['success']:
                    st.success("✅ データの読み込みに成功しました")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        wardrobe_items = sum(
                            len(items) for items in result['wardrobe'].values()
                        )
                        st.metric("ワードローブアイテム", wardrobe_items)
                    
                    with col2:
                        st.metric("コーディネート履歴", len(result['history']))
                    
                    if st.button("📥 このデータをインポートする (ZIP)", type="primary"):
                        # ワードローブを更新
                        manager.wardrobe = result['wardrobe']
                        manager._save_wardrobe()
                        
                        # 履歴を更新
                        history_manager.history = result['history']
                        history_manager._save_history()
                        
                        st.success("✅ データをインポートしました！")
                        st.rerun()
                
                else:
                    st.error(f"❌ エラー: {result['error']}")
            
            except Exception as e:
                st.error(f"❌ ファイルの読み込みに失敗しました: {str(e)}")


def main():
    """メインアプリケーション"""
    initialize_session_state()
    
    # モバイルフレンドリーなナビゲーション（上部に配置）
    st.markdown("""
    <style>
    /* ナビゲーションボタン風 */
    div[data-testid="stHorizontalBlock"] button {
        width: 100%;
        border-radius: 10px;
        font-size: 0.9rem;
        padding: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # トップナビゲーション（6つに拡張）
    nav_cols = st.columns(6)
    
    with nav_cols[0]:
        if st.button("🏠\nホーム", key="nav_home"):
            st.session_state.page = "🏠 ホーム"
    with nav_cols[1]:
        if st.button("💖\nお気に入り", key="nav_favorite"):
            st.session_state.page = "💖 お気に入りコーデ"
    with nav_cols[2]:
        if st.button("👗\n服", key="nav_wardrobe"):
            st.session_state.page = "👗 ワードローブ管理"
    with nav_cols[3]:
        if st.button("🛍️\n買物", key="nav_shop"):
            st.session_state.page = "🛍️ 新しい服を探す"
    with nav_cols[4]:
        if st.button("📊\n履歴", key="nav_history"):
            st.session_state.page = "📊 履歴"
    with nav_cols[5]:
        if st.button("💾\nデータ", key="nav_data"):
            st.session_state.page = "💾 データ管理"
    
    # デフォルトページ
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 ホーム"
    
    page = st.session_state.page
    
    st.markdown("---")
    
    # ページルーティング
    if page == "🏠 ホーム":
        main_page()
    elif page == "💖 お気に入りコーデ":
        favorite_item_outfit_page()
    elif page == "👗 ワードローブ管理":
        wardrobe_management_page()
    elif page == "🛍️ 新しい服を探す":
        shopping_page()
    elif page == "📊 履歴":
        history_page()
    elif page == "💾 データ管理":
        data_management_page()


if __name__ == "__main__":
    main()
