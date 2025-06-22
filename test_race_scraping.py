#!/usr/bin/env python3
"""
レース情報取得とスプレッドシート連携のテストスクリプト
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.scraping.race_scraper import RaceScraper
from src.data.spreadsheet_manager import SpreadsheetManager
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_race_scraping():
    """レース情報取得のテスト"""
    print("=== レース情報取得テスト ===")
    
    try:
        scraper = RaceScraper()
        races = scraper.get_high_odds_races()
        
        print(f"取得したレース数: {len(races)}")
        
        for i, race in enumerate(races, 1):
            print(f"\n[レース {i}]")
            print(f"レース名: {race['race_name']}")
            print(f"開催日: {race['race_date']}")
            print(f"時刻: {race['race_time']}")
            print(f"会場: {race['venue']}")
            print(f"予想配当: {race['expected_odds']}倍")
            print(f"URL: {race['race_url']}")
        
        return races
        
    except Exception as e:
        print(f"エラー: {e}")
        return []

def test_spreadsheet_connection():
    """スプレッドシート接続テスト"""
    print("\n=== スプレッドシート接続テスト ===")
    
    try:
        manager = SpreadsheetManager()
        
        # 接続テスト
        if manager.test_connection():
            print("✅ スプレッドシート接続成功")
            
            # 統計情報を取得
            stats = manager.get_statistics()
            if stats:
                print(f"総レース数: {stats.get('total_races', 0)}")
                print(f"的中レース数: {stats.get('hit_races', 0)}")
                print(f"的中率: {stats.get('hit_rate', 0):.1f}%")
            
            return manager
        else:
            print("❌ スプレッドシート接続失敗")
            return None
            
    except Exception as e:
        print(f"❌ スプレッドシートエラー: {e}")
        print("注意: Google認証情報を設定してください")
        return None

def test_data_recording(races, manager):
    """データ記録テスト"""
    print("\n=== データ記録テスト ===")
    
    if not manager:
        print("スプレッドシートマネージャーが利用できません")
        return
    
    if not races:
        print("記録するレースデータがありません")
        return
    
    try:
        # 最初のレースを記録
        race = races[0]
        
        # テスト用の買い目データ
        bet_data = {
            'combination': '1-2-3',
            'bet_type': '3連単',
            'amount': 100
        }
        
        success = manager.record_prediction(race, bet_data)
        
        if success:
            print("✅ データ記録成功")
            print(f"記録したレース: {race['race_name']}")
        else:
            print("❌ データ記録失敗")
            
    except Exception as e:
        print(f"❌ データ記録エラー: {e}")

def main():
    """メイン処理"""
    print("ちょいアツ艇報 - システムテスト")
    print("=" * 40)
    
    # 1. レース情報取得テスト
    races = test_race_scraping()
    
    # 2. スプレッドシート接続テスト
    manager = test_spreadsheet_connection()
    
    # 3. データ記録テスト
    test_data_recording(races, manager)
    
    print("\n=== テスト完了 ===")

if __name__ == "__main__":
    main()