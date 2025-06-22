#!/usr/bin/env python3
"""
ちょいアツ艇報 - メインエントリーポイント
ボートレース予想通知システム
"""

import sys
import os
from datetime import datetime
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.scraping.race_scraper import RaceScraper
from src.prediction.bet_selector import BetSelector
from src.notification.line_notifier import LineNotifier
from src.data.spreadsheet_manager import SpreadsheetManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """メイン処理"""
    try:
        logger.info("ちょいアツ艇報システム開始")
        
        # 各コンポーネントの初期化
        scraper = RaceScraper()
        bet_selector = BetSelector()
        notifier = LineNotifier()
        spreadsheet = SpreadsheetManager()
        
        # 高配当レースの抽出
        races = scraper.get_high_odds_races()
        logger.info(f"高配当レース{len(races)}件を取得")
        
        # 買い目選定
        selected_bets = bet_selector.select_bets(races)
        logger.info(f"買い目{len(selected_bets)}件を選定")
        
        # LINE通知
        for bet in selected_bets:
            notifier.send_prediction(bet)
            spreadsheet.record_prediction(bet)
        
        logger.info("処理完了")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise

if __name__ == "__main__":
    main()