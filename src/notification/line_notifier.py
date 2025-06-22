"""
LINE通知クラス
ボートレース予想と結果をLINE公式アカウント経由で通知
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,
    BubbleContainer, BoxComponent, TextComponent, ButtonComponent,
    URIAction, MessageAction
)

from config.settings import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

logger = logging.getLogger(__name__)

class LineNotifier:
    """LINE通知を管理するクラス"""
    
    def __init__(self):
        if not LINE_CHANNEL_ACCESS_TOKEN or LINE_CHANNEL_ACCESS_TOKEN == 'your_line_channel_access_token_here':
            raise ValueError("LINE_CHANNEL_ACCESS_TOKENが設定されていません")
        
        self.line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(LINE_CHANNEL_SECRET)
        
        logger.info("LINE Bot API初期化完了")
    
    def send_prediction(self, race_data: Dict, bet_data: Optional[Dict] = None) -> bool:
        """
        予想通知を送信
        
        Args:
            race_data: レース情報
            bet_data: 買い目情報
            
        Returns:
            送信成功可否
        """
        try:
            # 予想メッセージを作成
            message = self._create_prediction_message(race_data, bet_data)
            
            # ブロードキャスト送信（全フォロワーに送信）
            self.line_bot_api.broadcast(message)
            
            logger.info(f"予想通知送信成功: {race_data.get('race_name')}")
            return True
            
        except LineBotApiError as e:
            logger.error(f"LINE API エラー: {e}")
            return False
        except Exception as e:
            logger.error(f"予想通知送信エラー: {e}")
            return False
    
    def send_result(self, race_data: Dict, result_data: Dict) -> bool:
        """
        結果通知を送信
        
        Args:
            race_data: レース情報
            result_data: 結果情報
            
        Returns:
            送信成功可否
        """
        try:
            # 結果メッセージを作成
            message = self._create_result_message(race_data, result_data)
            
            # ブロードキャスト送信
            self.line_bot_api.broadcast(message)
            
            logger.info(f"結果通知送信成功: {race_data.get('race_name')}")
            return True
            
        except LineBotApiError as e:
            logger.error(f"LINE API エラー: {e}")
            return False
        except Exception as e:
            logger.error(f"結果通知送信エラー: {e}")
            return False
    
    def send_test_message(self, message_text: str = "テスト通知") -> bool:
        """
        テスト通知を送信
        
        Args:
            message_text: 送信メッセージ
            
        Returns:
            送信成功可否
        """
        try:
            message = TextSendMessage(text=message_text)
            self.line_bot_api.broadcast(message)
            
            logger.info("テスト通知送信成功")
            return True
            
        except LineBotApiError as e:
            logger.error(f"テスト通知エラー: {e}")
            return False
        except Exception as e:
            logger.error(f"テスト通知エラー: {e}")
            return False
    
    def _create_prediction_message(self, race_data: Dict, bet_data: Optional[Dict]) -> FlexSendMessage:
        """予想通知のメッセージを作成"""
        
        # 絵文字とカジュアルな文言
        emojis = ["🚤", "💰", "🔥", "⚡", "🎯"]
        
        race_name = race_data.get('race_name', '')
        race_time = race_data.get('race_time', '')
        expected_odds = race_data.get('expected_odds', 0)
        race_url = race_data.get('race_url', '')
        bet_combination = bet_data.get('combination', '') if bet_data else ''
        
        # タイトル文言
        title = f"🚤 ちょいアツ予想 {emojis[len(race_name) % len(emojis)]}"
        
        # メインメッセージ
        main_text = f"今夜は{race_name}で攻めます！\n"
        main_text += f"⏰ {race_time}〜\n"
        main_text += f"💰 予想配当: {expected_odds}倍\n"
        
        if bet_combination:
            main_text += f"🎯 買い目: {bet_combination}\n"
        
        main_text += "\n熱くなりすぎず、ちょいアツで行きましょう✨"
        
        # Flex Message作成
        bubble = BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text=title,
                        weight="bold",
                        size="lg",
                        color="#FF6B35"
                    ),
                    TextComponent(
                        text=main_text,
                        size="md",
                        margin="md",
                        wrap=True
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    ButtonComponent(
                        style="primary",
                        color="#FF6B35",
                        action=URIAction(
                            label="レース詳細を見る",
                            uri=race_url
                        )
                    )
                ]
            ) if race_url else None
        )
        
        return FlexSendMessage(alt_text=f"予想通知: {race_name}", contents=bubble)
    
    def _create_result_message(self, race_data: Dict, result_data: Dict) -> FlexSendMessage:
        """結果通知のメッセージを作成"""
        
        race_name = race_data.get('race_name', '')
        result_order = result_data.get('result_order', [])
        payout = result_data.get('payout', {})
        
        # 結果判定
        sanrentan = payout.get('3連単', {})
        payout_amount = sanrentan.get('amount', 0)
        is_hit = payout_amount > 0
        
        # 演出選択
        if is_hit:
            if payout_amount >= 10000:
                title = "🎉 大勝利！！ 🎉"
                message = f"やりました！{payout_amount}円GET！\n"
                message += "今夜は焼肉だ〜 🍖✨"
                color = "#FF6B35"
            elif payout_amount >= 3000:
                title = "🎯 的中！ 🎯"
                message = f"ナイス！{payout_amount}円GET！\n"
                message += "ちょいアツ的中です 🔥"
                color = "#4CAF50"
            else:
                title = "✅ 的中"
                message = f"{payout_amount}円GET\n"
                message += "コツコツ行きましょう 💪"
                color = "#2196F3"
        else:
            # 惜しい判定（簡易版）
            title = "💔 不的中"
            message = "今回は残念でした...\n"
            message += "次回に期待！切り替えて行きます 🔄"
            color = "#9E9E9E"
        
        result_text = f"結果: {'-'.join(result_order)}"
        
        bubble = BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text=title,
                        weight="bold",
                        size="lg",
                        color=color
                    ),
                    TextComponent(
                        text=f"📍 {race_name}",
                        size="md",
                        margin="md"
                    ),
                    TextComponent(
                        text=result_text,
                        size="md",
                        margin="sm"
                    ),
                    TextComponent(
                        text=message,
                        size="md",
                        margin="md",
                        wrap=True
                    )
                ]
            )
        )
        
        return FlexSendMessage(alt_text=f"結果通知: {race_name}", contents=bubble)
    
    def get_follower_count(self) -> Optional[int]:
        """
        フォロワー数を取得
        
        Returns:
            フォロワー数
        """
        try:
            profile = self.line_bot_api.get_bot_info()
            # 注意: 実際のフォロワー数は別のAPIで取得する必要があります
            logger.info("Bot情報取得成功")
            return None  # フォロワー数は別途取得が必要
            
        except LineBotApiError as e:
            logger.error(f"Bot情報取得エラー: {e}")
            return None
    
    def validate_connection(self) -> bool:
        """
        LINE API接続テスト
        
        Returns:
            接続成功可否
        """
        try:
            # Bot情報を取得してテスト
            bot_info = self.line_bot_api.get_bot_info()
            logger.info(f"LINE Bot接続テスト成功: {bot_info.display_name}")
            return True
            
        except LineBotApiError as e:
            logger.error(f"LINE Bot接続テストエラー: {e}")
            return False
        except Exception as e:
            logger.error(f"LINE Bot接続テストエラー: {e}")
            return False