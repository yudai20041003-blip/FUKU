# 🚀 デプロイメントガイド

このアプリを公開するための様々な方法を紹介します。

## 📋 目次
1. [Streamlit Cloud（推奨・無料）](#1-streamlit-cloud推奨無料)
2. [GitHub Pages（静的サイト）](#2-github-pages静的サイト)
3. [Vercel（高速・無料）](#3-vercel高速無料)
4. [Render（簡単・無料）](#4-render簡単無料)
5. [Heroku（有料プランのみ）](#5-heroku有料プランのみ)
6. [Railway（モダン・無料）](#6-railwayモダン無料)
7. [自分のサーバー](#7-自分のサーバー)

---

## 1. Streamlit Cloud（推奨・無料）

### ✅ メリット
- **完全無料**
- **設定が超簡単**
- **Streamlit専用**で最適化
- 自動デプロイ
- HTTPS対応

### 📝 手順

1. **Streamlit Cloudにアクセス**
   ```
   https://streamlit.io/cloud
   ```

2. **GitHubでサインイン**
   - 「Sign in with GitHub」をクリック

3. **新しいアプリをデプロイ**
   - 「New app」をクリック
   - リポジトリ: `yudai20041003-blip/FUKU`
   - ブランチ: `genspark_ai_developer`
   - メインファイル: `app.py`
   - 「Deploy!」をクリック

4. **完了！**
   - 数分で公開URL取得: `https://your-app.streamlit.app`

### ⚙️ 設定（オプション）

`.streamlit/config.toml`を作成：
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
headless = true
port = 8501
```

---

## 2. GitHub Pages（静的サイト）

### ⚠️ 注意
Streamlitは動的アプリなので、GitHub Pagesには**そのままでは対応不可**。
静的HTML版を作る必要があります。

### 代替案
- Streamlitではなく、React/Vue.jsで再構築
- または他のサービスを使用

---

## 3. Vercel（高速・無料）

### ✅ メリット
- **超高速デプロイ**
- **無料プラン充実**
- 自動HTTPS
- カスタムドメイン対応

### ⚠️ 注意
Streamlitは直接サポートされていないため、FastAPI版への変換が必要

### 📝 手順（FastAPI版を作る場合）

1. **Vercelにサインアップ**
   ```
   https://vercel.com
   ```

2. **GitHubと連携**
   - 「Import Project」
   - GitHubリポジトリを選択

3. **設定**
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`

---

## 4. Render（簡単・無料）

### ✅ メリット
- **Streamlit公式サポート**
- **完全無料プラン**
- 自動デプロイ
- HTTPS対応
- 設定が簡単

### 📝 手順

1. **Renderにサインアップ**
   ```
   https://render.com
   ```

2. **新しいWeb Serviceを作成**
   - 「New」→「Web Service」をクリック
   - GitHubリポジトリを接続

3. **設定**
   ```
   Name: fashion-coordinator
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

4. **デプロイ**
   - 「Create Web Service」をクリック
   - 自動的にデプロイ開始

5. **完了！**
   - URL: `https://fashion-coordinator.onrender.com`

### 💰 料金
- **Free Tier**: 無料（スリープあり）
- **Starter**: $7/月（常時起動）

---

## 5. Heroku（有料プランのみ）

### ⚠️ 注意
2022年11月より**無料プランが廃止**されました。

### 💰 料金
- **Basic**: $7/月〜
- **Production**: $25/月〜

### 📝 手順（有料プラン使用時）

1. **Herokuにサインアップ**
   ```
   https://heroku.com
   ```

2. **Heroku CLIをインストール**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **ログイン**
   ```bash
   heroku login
   ```

4. **アプリを作成**
   ```bash
   heroku create fashion-coordinator
   ```

5. **デプロイ**
   ```bash
   git push heroku genspark_ai_developer:main
   ```

---

## 6. Railway（モダン・無料）

### ✅ メリット
- **モダンなUI**
- **無料枠あり**（$5クレジット/月）
- GitHubと自動連携
- 簡単な設定

### 📝 手順

1. **Railwayにサインアップ**
   ```
   https://railway.app
   ```

2. **新しいプロジェクトを作成**
   - 「New Project」をクリック
   - 「Deploy from GitHub repo」を選択
   - リポジトリを選択

3. **設定**
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

4. **環境変数を設定（オプション）**
   - `OPENWEATHER_API_KEY`: あなたのAPIキー

5. **デプロイ**
   - 自動的にデプロイされます

### 💰 料金
- **Trial**: $5クレジット/月（無料）
- **Developer**: $5/月（$5クレジット含む）

---

## 7. 自分のサーバー

### VPS（Virtual Private Server）を使う

#### おすすめVPS
- **さくらのVPS**: 月額685円〜
- **ConoHa VPS**: 月額968円〜
- **AWS Lightsail**: $3.50/月〜
- **DigitalOcean**: $6/月〜

### 📝 手順（例：Ubuntu Server）

1. **サーバーにSSH接続**
   ```bash
   ssh user@your-server-ip
   ```

2. **必要なパッケージをインストール**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git nginx -y
   ```

3. **リポジトリをクローン**
   ```bash
   cd /var/www
   sudo git clone https://github.com/yudai20041003-blip/FUKU.git
   cd FUKU
   sudo git checkout genspark_ai_developer
   ```

4. **依存関係をインストール**
   ```bash
   sudo pip3 install -r requirements.txt
   ```

5. **Systemdサービスを作成**
   ```bash
   sudo nano /etc/systemd/system/fashion-app.service
   ```
   
   内容：
   ```ini
   [Unit]
   Description=Fashion Coordinator App
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/var/www/FUKU
   ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **サービスを起動**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start fashion-app
   sudo systemctl enable fashion-app
   ```

7. **Nginxでリバースプロキシ設定**
   ```bash
   sudo nano /etc/nginx/sites-available/fashion-app
   ```
   
   内容：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

8. **Nginxを有効化**
   ```bash
   sudo ln -s /etc/nginx/sites-available/fashion-app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 🎯 推奨デプロイ方法まとめ

| サービス | 難易度 | 料金 | 速度 | おすすめ度 |
|---------|--------|------|------|-----------|
| **Streamlit Cloud** | ⭐ | 無料 | 普通 | ⭐⭐⭐⭐⭐ |
| **Render** | ⭐⭐ | 無料 | 速い | ⭐⭐⭐⭐ |
| **Railway** | ⭐⭐ | $5/月 | 速い | ⭐⭐⭐⭐ |
| **Vercel** | ⭐⭐⭐ | 無料 | 超速 | ⭐⭐⭐（要変換） |
| **Heroku** | ⭐⭐ | $7/月〜 | 普通 | ⭐⭐ |
| **自分のVPS** | ⭐⭐⭐⭐⭐ | 月額数百円〜 | 自由 | ⭐⭐⭐ |

---

## 🚀 今すぐ始めるなら

### 1位: Streamlit Cloud ⭐⭐⭐⭐⭐
**理由**: 完全無料、設定が超簡単、Streamlit専用

### 2位: Render ⭐⭐⭐⭐
**理由**: 無料、Streamlitサポート、簡単

### 3位: Railway ⭐⭐⭐⭐
**理由**: モダンなUI、月$5で十分

---

## ❓ よくある質問

**Q: 完全無料で公開できる？**
A: はい！Streamlit CloudまたはRenderの無料プランで可能です。

**Q: 独自ドメインは使える？**
A: はい。Streamlit Cloud、Render、Vercelなどで設定可能です。

**Q: どれくらいの人が同時にアクセスできる？**
A: 無料プランで数十〜数百人、有料プランで数千人以上対応できます。

**Q: HTTPSは使える？**
A: すべてのサービスで自動的にHTTPS対応されます。

---

## 📝 次のステップ

1. **Streamlit Cloudでデプロイ**（5分）
2. **独自ドメインを設定**（オプション）
3. **OpenWeatherMap APIキーを設定**（リアルタイム天気用）
4. **友達に共有！** 🎉

---

**おすすめ**: まずはStreamlit Cloudで試して、後から必要に応じて他のサービスに移行するのが良いでしょう！
