#!/usr/bin/env python3
"""
スプレッドシート状況確認用デバッグスクリプト
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data.spreadsheet_manager import SpreadsheetManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_spreadsheet():
    """スプレッドシートの状況を詳しく調査"""
    try:
        manager = SpreadsheetManager()
        
        print("=== スプレッドシート情報 ===")
        print(f"スプレッドシート名: {manager.spreadsheet.title}")
        print(f"スプレッドシートID: {manager.spreadsheet_id}")
        
        print("\n=== ワークシート一覧 ===")
        worksheets = manager.spreadsheet.worksheets()
        for i, ws in enumerate(worksheets):
            print(f"{i+1}. {ws.title} ({ws.row_count}行 x {ws.col_count}列)")
            
            # 各ワークシートの内容を確認
            try:
                if ws.row_count > 0:
                    values = ws.get_all_values()
                    if values:
                        print(f"   データ行数: {len(values)}")
                        if len(values) > 0:
                            print(f"   1行目: {values[0][:5]}")  # 最初の5列のみ表示
                        if len(values) > 1:
                            print(f"   2行目: {values[1][:5]}")  # 最初の5列のみ表示
                    else:
                        print("   データなし")
                else:
                    print("   空のワークシート")
            except Exception as e:
                print(f"   エラー: {e}")
        
        print(f"\n=== 現在使用中のワークシート ===")
        print(f"ワークシート名: {manager.worksheet.title}")
        
        # 現在のワークシートの全データを取得
        try:
            all_data = manager.worksheet.get_all_values()
            print(f"データ行数: {len(all_data)}")
            
            for i, row in enumerate(all_data[:5]):  # 最初の5行のみ表示
                print(f"行{i+1}: {row}")
                
        except Exception as e:
            print(f"データ取得エラー: {e}")
            
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        return False

def test_write():
    """テスト書き込み"""
    try:
        manager = SpreadsheetManager()
        
        print("\n=== テスト書き込み ===")
        
        # テストデータ
        test_race = {
            'race_date': '2025-06-22',
            'race_name': 'デバッグテスト1R',
            'venue': 'テスト会場',
            'race_number': 1,
            'race_time': '10:00',
            'grade': 'TEST',
            'expected_odds': 99.9,
            'race_url': 'https://test.com'
        }
        
        test_bet = {
            'combination': '1-2-3',
            'bet_type': '3連単',
            'amount': 100
        }
        
        success = manager.record_prediction(test_race, test_bet)
        print(f"書き込み結果: {'成功' if success else '失敗'}")
        
        # 書き込み後のデータ確認
        print("\n=== 書き込み後のデータ確認 ===")
        all_data = manager.worksheet.get_all_values()
        for i, row in enumerate(all_data[-3:]):  # 最後の3行のみ表示
            print(f"行{len(all_data)-2+i}: {row}")
            
    except Exception as e:
        print(f"テスト書き込みエラー: {e}")

if __name__ == "__main__":
    print("スプレッドシート デバッグツール")
    print("=" * 40)
    
    if debug_spreadsheet():
        test_write()