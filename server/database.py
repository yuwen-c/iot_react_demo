#!/usr/bin/env python3
"""
資料庫連接模組
處理 SQLite 資料庫連接和基本操作
"""

import sqlite3
import os
import sys
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

# 將專案根目錄加入 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import Config

class DatabaseManager:
    """資料庫管理類別"""
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化資料庫管理器"""
        self.db_path = db_path or Config.get_db_path()
        self._ensure_db_directory()
    
    def _ensure_db_directory(self):
        """確保資料庫目錄存在"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    @contextmanager
    def get_connection(self):
        """取得資料庫連接的上下文管理器"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            print(f"❌ 資料庫連接錯誤: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_latest_sensor_reading(self) -> Optional[Dict[str, Any]]:
        """取得最新的感測器讀數"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, temp, humidity, timestamp, created_at
                    FROM sensor_readings
                    ORDER BY created_at DESC
                    LIMIT 1
                """)
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"❌ 取得最新讀數失敗: {e}")
            return None
    
    def get_sensor_readings(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """取得感測器讀數列表"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, temp, humidity, timestamp, created_at
                    FROM sensor_readings
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """, (limit, offset))
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"❌ 取得讀數列表失敗: {e}")
            return []
    
    def get_sensor_readings_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """根據日期範圍取得感測器讀數"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, temp, humidity, timestamp, created_at
                    FROM sensor_readings
                    WHERE DATE(created_at) BETWEEN ? AND ?
                    ORDER BY created_at DESC
                """, (start_date, end_date))
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"❌ 取得日期範圍讀數失敗: {e}")
            return []
    
    def get_sensor_statistics(self) -> Dict[str, Any]:
        """取得感測器統計資訊"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 取得基本統計
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_readings,
                        AVG(temp) as avg_temp,
                        AVG(humidity) as avg_humidity,
                        MIN(temp) as min_temp,
                        MAX(temp) as max_temp,
                        MIN(humidity) as min_humidity,
                        MAX(humidity) as max_humidity
                    FROM sensor_readings
                """)
                stats = dict(cursor.fetchone())
                
                # 取得最新讀數時間
                cursor.execute("""
                    SELECT created_at
                    FROM sensor_readings
                    ORDER BY created_at DESC
                    LIMIT 1
                """)
                latest = cursor.fetchone()
                if latest:
                    stats['latest_reading_time'] = latest['created_at']
                
                return stats
        except Exception as e:
            print(f"❌ 取得統計資訊失敗: {e}")
            return {}
    
    def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """取得警報歷史"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, alert_type, severity, message, sensor_data, timestamp, sent_to_frontend, created_at
                    FROM alert_history
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (limit,))
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"❌ 取得警報歷史失敗: {e}")
            return []

# 建立全域資料庫管理器實例
db_manager = DatabaseManager()

def get_db_manager() -> DatabaseManager:
    """取得資料庫管理器實例"""
    return db_manager 