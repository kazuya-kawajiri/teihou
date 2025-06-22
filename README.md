# ちょいアツ艇報

ボートレース予想通知システム - 月額サブスクリプションサービス

## 概要

高配当が狙えるボートレースを自動で選定し、LINE公式アカウントを通じて買い目を通知するシステムです。

## 機能

- 50倍以上の高配当レース自動抽出
- 買い目自動選定
- LINE公式アカウント経由での通知
- 結果の自動取得と演出付き通知
- Googleスプレッドシートでの成果記録

## セットアップ

### 1. 環境設定

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp config/.env.example config/.env
# config/.envを編集して必要な値を設定
```

### 2. 必要な設定

- LINE公式アカウントのチャンネルアクセストークン
- Googleスプレッドシートの認証情報
- スプレッドシートID

### 3. 実行

```bash
python main.py
```

## プロジェクト構造

```
ちょいアツ艇報/
├── main.py                 # メインエントリーポイント
├── requirements.txt        # 依存関係
├── config/                 # 設定ファイル
│   ├── settings.py
│   └── .env.example
├── src/                    # ソースコード
│   ├── scraping/          # スクレイピング機能
│   ├── prediction/        # 予想ロジック
│   ├── notification/      # 通知機能
│   ├── data/             # データ管理
│   └── utils/            # ユーティリティ
├── logs/                  # ログファイル
├── data/                  # データファイル
└── tests/                 # テストコード
```

## 開発環境

- Python 3.8+
- Cursor + Claude Code
- GitHub連携

## 注意事項

- LINE通知は月1000通以下に抑制（無料枠内運用）
- スクレイピング時は適切な間隔を設けること
- 個人情報や認証情報は.envファイルで管理