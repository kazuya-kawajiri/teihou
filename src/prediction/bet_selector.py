"""
買い目選定クラス
高配当レースから最適な買い目を選定
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BetSelector:
    """買い目選定クラス"""
    
    def __init__(self):
        """初期化"""
        self.min_odds = 50.0  # 最小配当倍率
        self.max_bets_per_day = 3  # 1日最大買い目数
        
    def select_bets(self, races: List[Dict]) -> List[Dict]:
        """
        レース情報から買い目を選定
        
        Args:
            races: レース情報のリスト
            
        Returns:
            選定した買い目のリスト
        """
        try:
            logger.info(f"買い目選定開始: {len(races)}レース")
            
            # 高配当レースをフィルタリング
            high_odds_races = self._filter_high_odds_races(races)
            
            # 買い目を選定
            selected_bets = []
            for race in high_odds_races[:self.max_bets_per_day]:
                bet = self._generate_bet(race)
                if bet:
                    selected_bets.append(bet)
            
            logger.info(f"買い目選定完了: {len(selected_bets)}件")
            return selected_bets
            
        except Exception as e:
            logger.error(f"買い目選定エラー: {e}")
            return []
    
    def _filter_high_odds_races(self, races: List[Dict]) -> List[Dict]:
        """高配当レースをフィルタリング"""
        return [
            race for race in races 
            if race.get('expected_odds', 0) >= self.min_odds
        ]
    
    def _generate_bet(self, race: Dict) -> Optional[Dict]:
        """
        レース情報から買い目を生成
        
        Args:
            race: レース情報
            
        Returns:
            買い目情報
        """
        try:
            # 参加者情報を取得
            participants = race.get('participants', [])
            if len(participants) < 6:
                return None
            
            # 簡易的な買い目選定ロジック
            # 実際の実装では、より高度な分析を行う
            
            # A1レーサーを優先的に選定
            a1_racers = [p for p in participants if p.get('rating') == 'A1']
            a2_racers = [p for p in participants if p.get('rating') == 'A2']
            
            if len(a1_racers) >= 2:
                # A1レーサー中心の組み合わせ
                combination = self._create_combination_with_a1(a1_racers, participants)
            elif len(a1_racers) == 1 and len(a2_racers) >= 1:
                # A1とA2の組み合わせ
                combination = self._create_mixed_combination(a1_racers[0], a2_racers, participants)
            else:
                # 荒れレース用の組み合わせ
                combination = self._create_upset_combination(participants)
            
            # 買い目データを構築
            bet_data = {
                'race_info': race,
                'combination': combination,
                'bet_type': '3連単',
                'investment': 1000,  # 投資額（円）
                'expected_return': race.get('expected_odds', 0) * 1000,
                'confidence': self._calculate_confidence(race, combination),
                'created_at': datetime.now().isoformat()
            }
            
            return bet_data
            
        except Exception as e:
            logger.error(f"買い目生成エラー: {e}")
            return None
    
    def _create_combination_with_a1(self, a1_racers: List[Dict], all_participants: List[Dict]) -> str:
        """A1レーサー中心の組み合わせを作成"""
        if len(a1_racers) >= 2:
            # 1着-2着はA1レーサー、3着は他から選択
            first = a1_racers[0]['position']
            second = a1_racers[1]['position']
            third_candidates = [p['position'] for p in all_participants 
                              if p['position'] not in [first, second]]
            third = third_candidates[0] if third_candidates else 3
            return f"{first}-{second}-{third}"
        return "1-2-3"  # デフォルト
    
    def _create_mixed_combination(self, a1_racer: Dict, a2_racers: List[Dict], all_participants: List[Dict]) -> str:
        """A1とA2の混合組み合わせを作成"""
        first = a1_racer['position']
        second = a2_racers[0]['position']
        third_candidates = [p['position'] for p in all_participants 
                          if p['position'] not in [first, second]]
        third = third_candidates[0] if third_candidates else 3
        return f"{first}-{second}-{third}"
    
    def _create_upset_combination(self, participants: List[Dict]) -> str:
        """荒れレース用の組み合わせを作成"""
        # 下位レーサーを含む組み合わせで高配当を狙う
        positions = [p['position'] for p in participants]
        if len(positions) >= 6:
            # 3-4-5着付近の組み合わせで荒れを狙う
            return "3-4-5"
        return "1-2-3"  # デフォルト
    
    def _calculate_confidence(self, race: Dict, combination: str) -> float:
        """
        買い目の信頼度を計算
        
        Args:
            race: レース情報
            combination: 買い目組み合わせ
            
        Returns:
            信頼度（0.0-1.0）
        """
        confidence = 0.5  # ベース信頼度
        
        # グレードによる調整
        grade = race.get('grade', '')
        if grade == 'G1':
            confidence += 0.2
        elif grade == 'G2':
            confidence += 0.1
        
        # 予想配当による調整
        expected_odds = race.get('expected_odds', 0)
        if expected_odds > 100:
            confidence -= 0.1  # 高配当すぎる場合は信頼度を下げる
        elif 50 <= expected_odds <= 80:
            confidence += 0.1  # 適度な高配当は信頼度を上げる
        
        return max(0.0, min(1.0, confidence))  # 0.0-1.0の範囲に制限 