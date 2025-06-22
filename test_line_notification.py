#!/usr/bin/env python3
"""
LINE通知機能のテストスクリプト
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.notification.line_notifier import LineNotifier
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_line_connection():
    """LINE API接続テスト"""
    print("=== LINE API接続テスト ===")
    
    try:
        notifier = LineNotifier()
        
        # 接続テスト
        if notifier.validate_connection():
            print("✅ LINE API接続成功")
            return notifier
        else:
            print("❌ LINE API接続失敗")
            return None
            
    except ValueError as e:
        print(f"❌ 設定エラー: {e}")
        print("💡 config/.envファイルでLINE_CHANNEL_ACCESS_TOKENを設定してください")
        return None
    except Exception as e:
        print(f"❌ LINE接続エラー: {e}")
        return None

def test_simple_message(notifier):
    """シンプルメッセージ送信テスト"""
    print("\n=== シンプルメッセージ送信テスト ===")
    
    if not notifier:
        print("LINE Notifierが利用できません")
        return
    
    try:
        message = "🚤 ちょいアツ艇報 - テスト通知です！"
        success = notifier.send_test_message(message)
        
        if success:
            print("✅ テスト通知送信成功")
            print("📱 LINE公式アカウントを確認してください")
        else:
            print("❌ テスト通知送信失敗")
            
    except Exception as e:
        print(f"❌ テスト通知エラー: {e}")

def test_prediction_message(notifier):
    """予想通知メッセージテスト"""
    print("\n=== 予想通知メッセージテスト ===")
    
    if not notifier:
        print("LINE Notifierが利用できません")
        return
    
    try:
        # テスト用レースデータ
        test_race = {
            'race_name': '住之江12R',
            'race_date': '2025-06-23',
            'race_time': '20:25',
            'venue': '住之江',
            'expected_odds': 65.2,
            'race_url': 'https://www.boatrace.jp/owpc/pc/race/racelist?rno=12&jcd=06&hd=20241223'
        }
        
        # テスト用買い目データ
        test_bet = {
            'combination': '1-3-2',
            'bet_type': '3連単',
            'amount': 100
        }
        
        success = notifier.send_prediction(test_race, test_bet)
        
        if success:
            print("✅ 予想通知送信成功")
            print("📱 LINE公式アカウントでFlexメッセージを確認してください")
        else:
            print("❌ 予想通知送信失敗")
            
    except Exception as e:
        print(f"❌ 予想通知エラー: {e}")

def test_result_message(notifier):
    """結果通知メッセージテスト"""
    print("\n=== 結果通知メッセージテスト ===")
    
    if not notifier:
        print("LINE Notifierが利用できません")
        return
    
    try:
        # テスト用レースデータ
        test_race = {
            'race_name': '住之江12R',
            'race_date': '2025-06-23',
            'race_time': '20:25',
            'venue': '住之江'
        }
        
        # テスト用結果データ（的中パターン）
        test_result_hit = {
            'result_order': ['1', '3', '2'],
            'payout': {
                '3連単': {
                    'combination': '1-3-2',
                    'odds': 45.6,
                    'amount': 4560
                }
            }
        }
        
        # テスト用結果データ（不的中パターン）
        test_result_miss = {
            'result_order': ['2', '1', '4'],
            'payout': {
                '3連単': {
                    'combination': '2-1-4',
                    'odds': 0,
                    'amount': 0
                }
            }
        }
        
        # 的中パターンテスト
        print("\n--- 的中パターン ---")
        success1 = notifier.send_result(test_race, test_result_hit)
        
        # 不的中パターンテスト
        print("--- 不的中パターン ---")
        success2 = notifier.send_result(test_race, test_result_miss)
        
        if success1 and success2:
            print("✅ 結果通知送信成功（両パターン）")
            print("📱 LINE公式アカウントで結果メッセージを確認してください")
        else:
            print("❌ 結果通知送信に問題があります")
            
    except Exception as e:
        print(f"❌ 結果通知エラー: {e}")

def main():
    """メイン処理"""
    print("ちょいアツ艇報 - LINE通知テスト")
    print("=" * 40)
    
    # 1. 接続テスト
    notifier = test_line_connection()
    
    # 2. シンプルメッセージテスト
    test_simple_message(notifier)
    
    # 3. 予想通知テスト
    test_prediction_message(notifier)
    
    # 4. 結果通知テスト
    test_result_message(notifier)
    
    print("\n=== テスト完了 ===")
    print("📱 LINE公式アカウントで通知を確認してください")

if __name__ == "__main__":
    main()