# ちょいアツ艇報 - 設定情報まとめ

## プロジェクト概要
- **プロジェクト名**: ちょいアツ艇報
- **目的**: ボートレース予想通知システム（月額サブスクリプションサービス）
- **GitHub**: https://github.com/kazuya-kawajiri/teihou.git
- **開発者**: kk020 (kk0204777@gmail.com)

## LINE API設定
### LINE公式アカウント
- **アカウント名**: ちょいアツ艇報通知
- **LINE ID**: @352kydmr
- **管理画面**: https://manager.line.biz/account/@352kydmr

### LINE Developers設定
- **プロバイダー名**: ちょいアツ艇報
- **Channel ID**: 2007619626
- **Channel Secret**: 359ac5dd22d77c096463491ded543a5e
- **Channel Access Token**: yX+9cAtY2uV1jGwdki3ADTffspznrz6qZMfgjztVDslLVkNoxCUbWKPcLZnyqreSwKa9nYYbKiQYQ2DA/8z/rQTDDe0XjMbOIP4Lk/9dc91HsES94kvRyysLXmx6lmkeiYKApL96ztSg1rLqVF9x0QdB04t89/1O/w1cDnyilFU=

## Google Cloud設定
### プロジェクト情報
- **プロジェクト名**: choiatsu-teiho
- **サービスアカウント**: choiatsu-teiho-service@choiatsu-teiho.iam.gserviceaccount.com
- **認証ファイル**: config/service_account.json (設置済み)

### Google Sheets API
- **有効化**: 完了
- **認証**: サービスアカウントキー方式
- **月間制限**: 100,000リクエスト（無料枠）

## システム構成
### 実装状況
- ✅ GitHub連携
- ✅ Google Sheets API連携（書き込みテスト成功）
- ✅ スプレッドシート管理クラス
- ✅ スクレイピング基盤（ダミーデータ）
- ✅ LINE API設定
- ⏳ LINE通知機能（未実装）
- ⏳ 買い目選定ロジック（未実装）
- ⏳ 実際のスクレイピング（未実装）

### 次の開発優先順位
1. LINE通知機能の実装
2. 買い目選定ロジックの実装
3. 実際のスクレイピング機能
4. スケジューリング機能

## 環境変数設定 (.env ファイル)
```env
# ちょいアツ艇報システム設定ファイル
# 作成日: 2024年12月23日

# LINE Messaging API設定
LINE_CHANNEL_ACCESS_TOKEN=yX+9cAtY2uV1jGwdki3ADTffspznrz6qZMfgjztVDslLVkNoxCUbWKPcLZnyqreSwKa9nYYbKiQYQ2DA/8z/rQTDDe0XjMbOIP4Lk/9dc91HsES94kvRyysLXmx6lmkeiYKApL96ztSg1rLqVF9x0QdB04t89/1O/w1cDnyilFU=
LINE_CHANNEL_SECRET=359ac5dd22d77c096463491ded543a5e
LINE_CHANNEL_ID=2007619626

# Google Sheets API設定
GOOGLE_CREDENTIALS_PATH=config/service_account.json
SPREADSHEET_ID=【あなたのスプレッドシートIDを入力】

# その他の設定
LOG_LEVEL=INFO
```

## セキュリティ設定
- **認証情報**: .envファイルで管理
- **.gitignore**: 設定済み（service_account.json、.env除外）
- **無料枠運用**: LINE月1000通以下、Google API月100,000リクエスト以下

## 開発環境
- **言語**: Python 3.8+
- **エディタ**: Cursor + Claude Code
- **OS**: WSL2 Ubuntu 22.04
- **依存関係**: requirements.txt設定済み

## テスト手順
### LINE通知テスト
1. LINE公式アカウント「@352kydmr」を友だち追加
2. 通知機能のテストメッセージ送信
3. メッセージ受信確認

### スプレッドシート連携テスト
1. 既に書き込みテスト成功済み
2. レース情報記録機能動作確認済み

---
最終更新: 2024年12月23日 