"""
Googleスプレッドシート管理クラス
レース情報と結果の記録を管理
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging
import json
import os

from config.settings import GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID

logger = logging.getLogger(__name__)

class SpreadsheetManager:
    """Googleスプレッドシートの管理クラス"""
    
    def __init__(self):
        self.spreadsheet_id = SPREADSHEET_ID
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self._authenticate()
    
    def _authenticate(self):
        """Google Sheets APIの認証"""
        try:
            # 認証情報の読み込み
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            if os.path.exists(GOOGLE_CREDENTIALS_PATH):
                # サービスアカウントキーファイルを使用
                creds = Credentials.from_service_account_file(
                    GOOGLE_CREDENTIALS_PATH, scopes=scope
                )
            else:
                # 環境変数から認証情報を取得（Heroku等での運用時）
                creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
                if creds_json:
                    creds_dict = json.loads(creds_json)
                    creds = Credentials.from_service_account_info(
                        creds_dict, scopes=scope
                    )
                else:
                    raise ValueError("Google認証情報が見つかりません")
            
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
            # デフォルトワークシートを取得（なければ作成）
            try:
                self.worksheet = self.spreadsheet.worksheet('レース記録')
            except gspread.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title='レース記録', rows=1000, cols=20
                )
                self._setup_headers()
            
            logger.info("Googleスプレッドシート認証成功")
            
        except Exception as e:
            logger.error(f"スプレッドシート認証エラー: {e}")
            raise
    
    def _setup_headers(self):
        """ヘッダー行を設定"""
        headers = [
            '日付', 'レース名', '会場', 'レース番号', '開始時刻',
            'グレード', '予想配当', '買い目', '結果', '的中',
            '配当金', '通知日時', 'レースURL', '備考'
        ]
        
        try:
            self.worksheet.insert_row(headers, 1)
            logger.info("ヘッダー行を設定しました")
        except Exception as e:
            logger.error(f"ヘッダー設定エラー: {e}")
    
    def record_prediction(self, race_data: Dict, bet_data: Optional[Dict] = None) -> bool:
        """
        予想データを記録
        
        Args:
            race_data: レース情報
            bet_data: 買い目情報
            
        Returns:
            記録成功可否
        """
        try:
            # データ行を準備
            row_data = [
                race_data.get('race_date', ''),
                race_data.get('race_name', ''),
                race_data.get('venue', ''),
                race_data.get('race_number', ''),
                race_data.get('race_time', ''),
                race_data.get('grade', ''),
                race_data.get('expected_odds', ''),
                bet_data.get('combination', '') if bet_data else '',
                '',  # 結果（後で更新）
                '',  # 的中（後で更新）
                '',  # 配当金（後で更新）
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                race_data.get('race_url', ''),
                ''   # 備考
            ]
            
            # 行を追加
            self.worksheet.append_row(row_data)
            logger.info(f"予想データを記録: {race_data.get('race_name')}")
            return True
            
        except Exception as e:
            logger.error(f"予想データ記録エラー: {e}")
            return False
    
    def update_result(self, race_name: str, result_data: Dict) -> bool:
        """
        結果を更新
        
        Args:
            race_name: レース名
            result_data: 結果データ
            
        Returns:
            更新成功可否
        """
        try:
            # レース名で該当行を検索
            cell = self.worksheet.find(race_name)
            if not cell:
                logger.warning(f"レースが見つかりません: {race_name}")
                return False
            
            row_num = cell.row
            
            # 結果データを更新
            result_order = '-'.join(result_data.get('result_order', []))
            payout_info = result_data.get('payout', {})
            
            # 3連単の配当情報を取得
            sanrentan = payout_info.get('3連単', {})
            payout_odds = sanrentan.get('odds', 0)
            payout_amount = sanrentan.get('amount', 0)
            
            # 的中判定（簡易版）
            is_hit = payout_amount > 0
            
            # セルを更新
            updates = [
                {'range': f'I{row_num}', 'values': [[result_order]]},      # 結果
                {'range': f'J{row_num}', 'values': [['○' if is_hit else '×']]},  # 的中
                {'range': f'K{row_num}', 'values': [[payout_amount]]},     # 配当金
            ]
            
            self.worksheet.batch_update(updates)
            logger.info(f"結果を更新: {race_name}")
            return True
            
        except Exception as e:
            logger.error(f"結果更新エラー: {e}")
            return False
    
    def get_recent_records(self, limit: int = 10) -> List[Dict]:
        """
        最近の記録を取得
        
        Args:
            limit: 取得件数
            
        Returns:
            記録のリスト
        """
        try:
            # 全データを取得
            records = self.worksheet.get_all_records()
            
            # 最新の記録を取得
            recent_records = records[-limit:] if len(records) > limit else records
            
            logger.info(f"最近の記録 {len(recent_records)} 件を取得")
            return recent_records
            
        except Exception as e:
            logger.error(f"記録取得エラー: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        統計情報を取得
        
        Returns:
            統計データ
        """
        try:
            records = self.worksheet.get_all_records()
            
            if not records:
                return {}
            
            total_races = len(records)
            hit_races = len([r for r in records if r.get('的中') == '○'])
            total_payout = sum([
                r.get('配当金', 0) for r in records 
                if isinstance(r.get('配当金'), (int, float))
            ])
            
            stats = {
                'total_races': total_races,
                'hit_races': hit_races,
                'hit_rate': (hit_races / total_races * 100) if total_races > 0 else 0,
                'total_payout': total_payout,
                'average_payout': (total_payout / hit_races) if hit_races > 0 else 0
            }
            
            logger.info("統計情報を取得しました")
            return stats
            
        except Exception as e:
            logger.error(f"統計取得エラー: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """
        接続テスト
        
        Returns:
            接続成功可否
        """
        try:
            # スプレッドシートの情報を取得してテスト
            title = self.spreadsheet.title
            logger.info(f"接続テスト成功: {title}")
            return True
            
        except Exception as e:
            logger.error(f"接続テストエラー: {e}")
            return False