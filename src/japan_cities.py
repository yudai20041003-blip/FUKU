"""
日本全国の都市データベース
47都道府県と主要都市の地点情報
"""

# 47都道府県の都市データ
JAPAN_CITIES = {
    # 北海道地方
    '北海道': {
        '札幌市': 'Sapporo',
        '函館市': 'Hakodate',
        '旭川市': 'Asahikawa',
        '釧路市': 'Kushiro',
        '帯広市': 'Obihiro',
        '北見市': 'Kitami',
        '小樽市': 'Otaru'
    },
    
    # 東北地方
    '青森県': {
        '青森市': 'Aomori',
        '八戸市': 'Hachinohe',
        '弘前市': 'Hirosaki'
    },
    '岩手県': {
        '盛岡市': 'Morioka',
        '一関市': 'Ichinoseki',
        '奥州市': 'Oshu'
    },
    '宮城県': {
        '仙台市': 'Sendai',
        '石巻市': 'Ishinomaki',
        '大崎市': 'Osaki'
    },
    '秋田県': {
        '秋田市': 'Akita',
        '横手市': 'Yokote',
        '大館市': 'Odate'
    },
    '山形県': {
        '山形市': 'Yamagata',
        '米沢市': 'Yonezawa',
        '鶴岡市': 'Tsuruoka',
        '酒田市': 'Sakata'
    },
    '福島県': {
        '福島市': 'Fukushima',
        '郡山市': 'Koriyama',
        'いわき市': 'Iwaki',
        '会津若松市': 'Aizuwakamatsu'
    },
    
    # 関東地方
    '茨城県': {
        '水戸市': 'Mito',
        'つくば市': 'Tsukuba',
        '日立市': 'Hitachi',
        '土浦市': 'Tsuchiura'
    },
    '栃木県': {
        '宇都宮市': 'Utsunomiya',
        '小山市': 'Oyama',
        '栃木市': 'Tochigi',
        '日光市': 'Nikko'
    },
    '群馬県': {
        '前橋市': 'Maebashi',
        '高崎市': 'Takasaki',
        '太田市': 'Ota',
        '伊勢崎市': 'Isesaki'
    },
    '埼玉県': {
        'さいたま市': 'Saitama',
        '川口市': 'Kawaguchi',
        '川越市': 'Kawagoe',
        '所沢市': 'Tokorozawa',
        '越谷市': 'Koshigaya',
        '草加市': 'Soka'
    },
    '千葉県': {
        '千葉市': 'Chiba',
        '船橋市': 'Funabashi',
        '松戸市': 'Matsudo',
        '市川市': 'Ichikawa',
        '柏市': 'Kashiwa',
        '成田市': 'Narita'
    },
    '東京都': {
        '千代田区': 'Chiyoda',
        '中央区': 'Chuo',
        '港区': 'Minato',
        '新宿区': 'Shinjuku',
        '渋谷区': 'Shibuya',
        '品川区': 'Shinagawa',
        '世田谷区': 'Setagaya',
        '練馬区': 'Nerima',
        '江戸川区': 'Edogawa',
        '八王子市': 'Hachioji',
        '立川市': 'Tachikawa',
        '町田市': 'Machida'
    },
    '神奈川県': {
        '横浜市': 'Yokohama',
        '川崎市': 'Kawasaki',
        '相模原市': 'Sagamihara',
        '横須賀市': 'Yokosuka',
        '鎌倉市': 'Kamakura',
        '藤沢市': 'Fujisawa',
        '小田原市': 'Odawara'
    },
    
    # 中部地方
    '新潟県': {
        '新潟市': 'Niigata',
        '長岡市': 'Nagaoka',
        '上越市': 'Joetsu',
        '三条市': 'Sanjo'
    },
    '富山県': {
        '富山市': 'Toyama',
        '高岡市': 'Takaoka',
        '魚津市': 'Uozu'
    },
    '石川県': {
        '金沢市': 'Kanazawa',
        '小松市': 'Komatsu',
        '加賀市': 'Kaga',
        '輪島市': 'Wajima'
    },
    '福井県': {
        '福井市': 'Fukui',
        '敦賀市': 'Tsuruga',
        '小浜市': 'Obama'
    },
    '山梨県': {
        '甲府市': 'Kofu',
        '富士吉田市': 'Fujiyoshida',
        '南アルプス市': 'Minamialps'
    },
    '長野県': {
        '長野市': 'Nagano',
        '松本市': 'Matsumoto',
        '上田市': 'Ueda',
        '飯田市': 'Iida',
        '諏訪市': 'Suwa',
        '軽井沢町': 'Karuizawa'
    },
    '岐阜県': {
        '岐阜市': 'Gifu',
        '大垣市': 'Ogaki',
        '高山市': 'Takayama',
        '多治見市': 'Tajimi'
    },
    '静岡県': {
        '静岡市': 'Shizuoka',
        '浜松市': 'Hamamatsu',
        '沼津市': 'Numazu',
        '富士市': 'Fuji',
        '熱海市': 'Atami',
        '伊東市': 'Ito'
    },
    '愛知県': {
        '名古屋市': 'Nagoya',
        '豊田市': 'Toyota',
        '岡崎市': 'Okazaki',
        '一宮市': 'Ichinomiya',
        '豊橋市': 'Toyohashi',
        '春日井市': 'Kasugai'
    },
    
    # 近畿地方
    '三重県': {
        '津市': 'Tsu',
        '四日市市': 'Yokkaichi',
        '伊勢市': 'Ise',
        '松阪市': 'Matsusaka',
        '鈴鹿市': 'Suzuka'
    },
    '滋賀県': {
        '大津市': 'Otsu',
        '草津市': 'Kusatsu',
        '彦根市': 'Hikone',
        '長浜市': 'Nagahama'
    },
    '京都府': {
        '京都市': 'Kyoto',
        '宇治市': 'Uji',
        '舞鶴市': 'Maizuru',
        '福知山市': 'Fukuchiyama'
    },
    '大阪府': {
        '大阪市': 'Osaka',
        '堺市': 'Sakai',
        '東大阪市': 'Higashiosaka',
        '豊中市': 'Toyonaka',
        '吹田市': 'Suita',
        '高槻市': 'Takatsuki',
        '枚方市': 'Hirakata'
    },
    '兵庫県': {
        '神戸市': 'Kobe',
        '姫路市': 'Himeji',
        '西宮市': 'Nishinomiya',
        '尼崎市': 'Amagasaki',
        '明石市': 'Akashi',
        '加古川市': 'Kakogawa',
        '宝塚市': 'Takarazuka'
    },
    '奈良県': {
        '奈良市': 'Nara',
        '橿原市': 'Kashihara',
        '生駒市': 'Ikoma',
        '大和郡山市': 'Yamatokoriyama'
    },
    '和歌山県': {
        '和歌山市': 'Wakayama',
        '田辺市': 'Tanabe',
        '橋本市': 'Hashimoto',
        '新宮市': 'Shingu'
    },
    
    # 中国地方
    '鳥取県': {
        '鳥取市': 'Tottori',
        '米子市': 'Yonago',
        '倉吉市': 'Kurayoshi'
    },
    '島根県': {
        '松江市': 'Matsue',
        '出雲市': 'Izumo',
        '浜田市': 'Hamada',
        '益田市': 'Masuda'
    },
    '岡山県': {
        '岡山市': 'Okayama',
        '倉敷市': 'Kurashiki',
        '津山市': 'Tsuyama',
        '玉野市': 'Tamano'
    },
    '広島県': {
        '広島市': 'Hiroshima',
        '福山市': 'Fukuyama',
        '呉市': 'Kure',
        '東広島市': 'Higashihiroshima',
        '尾道市': 'Onomichi'
    },
    '山口県': {
        '山口市': 'Yamaguchi',
        '下関市': 'Shimonoseki',
        '宇部市': 'Ube',
        '周南市': 'Shunan',
        '岩国市': 'Iwakuni'
    },
    
    # 四国地方
    '徳島県': {
        '徳島市': 'Tokushima',
        '阿南市': 'Anan',
        '鳴門市': 'Naruto'
    },
    '香川県': {
        '高松市': 'Takamatsu',
        '丸亀市': 'Marugame',
        '坂出市': 'Sakaide'
    },
    '愛媛県': {
        '松山市': 'Matsuyama',
        '今治市': 'Imabari',
        '宇和島市': 'Uwajima',
        '新居浜市': 'Niihama'
    },
    '高知県': {
        '高知市': 'Kochi',
        '南国市': 'Nankoku',
        '四万十市': 'Shimanto'
    },
    
    # 九州・沖縄地方
    '福岡県': {
        '福岡市': 'Fukuoka',
        '北九州市': 'Kitakyushu',
        '久留米市': 'Kurume',
        '飯塚市': 'Iizuka',
        '大牟田市': 'Omuta',
        '春日市': 'Kasuga'
    },
    '佐賀県': {
        '佐賀市': 'Saga',
        '唐津市': 'Karatsu',
        '鳥栖市': 'Tosu'
    },
    '長崎県': {
        '長崎市': 'Nagasaki',
        '佐世保市': 'Sasebo',
        '諫早市': 'Isahaya',
        '大村市': 'Omura'
    },
    '熊本県': {
        '熊本市': 'Kumamoto',
        '八代市': 'Yatsushiro',
        '天草市': 'Amakusa',
        '玉名市': 'Tamana'
    },
    '大分県': {
        '大分市': 'Oita',
        '別府市': 'Beppu',
        '中津市': 'Nakatsu',
        '日田市': 'Hita'
    },
    '宮崎県': {
        '宮崎市': 'Miyazaki',
        '都城市': 'Miyakonojo',
        '延岡市': 'Nobeoka',
        '日向市': 'Hyuga'
    },
    '鹿児島県': {
        '鹿児島市': 'Kagoshima',
        '霧島市': 'Kirishima',
        '鹿屋市': 'Kanoya',
        '薩摩川内市': 'Satsumasendai',
        '奄美市': 'Amami'
    },
    '沖縄県': {
        '那覇市': 'Naha',
        '沖縄市': 'Okinawa',
        '浦添市': 'Urasoe',
        '宜野湾市': 'Ginowan',
        '名護市': 'Nago',
        '石垣市': 'Ishigaki'
    }
}


def get_all_prefectures():
    """すべての都道府県を取得"""
    return list(JAPAN_CITIES.keys())


def get_cities_by_prefecture(prefecture):
    """都道府県内の都市を取得"""
    return JAPAN_CITIES.get(prefecture, {})


def get_all_cities_flat():
    """すべての都市を平坦なリストで取得"""
    cities = []
    for prefecture, city_dict in JAPAN_CITIES.items():
        for jp_name, en_name in city_dict.items():
            cities.append({
                'prefecture': prefecture,
                'jp_name': jp_name,
                'en_name': en_name
            })
    return cities


def search_city(query):
    """都市を検索"""
    results = []
    query_lower = query.lower()
    
    for prefecture, city_dict in JAPAN_CITIES.items():
        for jp_name, en_name in city_dict.items():
            if (query_lower in jp_name.lower() or 
                query_lower in en_name.lower() or
                query_lower in prefecture.lower()):
                results.append({
                    'prefecture': prefecture,
                    'jp_name': jp_name,
                    'en_name': en_name
                })
    
    return results


def translate_city_to_english(jp_city_name):
    """日本語の都市名を英語に変換"""
    for prefecture, city_dict in JAPAN_CITIES.items():
        if jp_city_name in city_dict:
            return city_dict[jp_city_name]
    
    # 見つからない場合はそのまま返す
    return jp_city_name
