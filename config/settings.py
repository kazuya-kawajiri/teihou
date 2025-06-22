"""
設定ファイル - ちょいアツ艇報
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).parent.parent

# LINE Messaging API設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# Googleスプレッドシート設定
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'config/service_account.json')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

# スクレイピング設定
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
REQUEST_DELAY = 1  # リクエスト間隔（秒）
SELENIUM_HEADLESS = True

# ボートレース関連設定
TARGET_ODDS_THRESHOLD = 50.0  # 対象とする最小配当倍率
MAX_RACES_PER_DAY = 3  # 1日あたりの最大レース数

# 通知設定
NOTIFICATION_SCHEDULE = {
    'prediction': '20:00',  # 予想通知時刻
    'result': '21:30'       # 結果通知時刻
}

# ログ設定
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = BASE_DIR / 'logs' / 'choiatsu_teiho.log'

# データディレクトリ
DATA_DIR = BASE_DIR / 'data'
ASSETS_DIR = BASE_DIR / 'assets'

# 環境変数チェック
def validate_config():
    """必要な環境変数が設定されているかチェック"""
    required_vars = [
        'LINE_CHANNEL_ACCESS_TOKEN',
        'LINE_CHANNEL_SECRET',
        'SPREADSHEET_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"環境変数が設定されていません: {', '.join(missing_vars)}")
    
    return True