#!/usr/bin/env python3
"""
Controller 資料庫管理模組
負責寫入感測器數據和警報記錄到共享 SQLite 資料庫
"""

import sqlite3
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# 加入專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        """初始化資料庫管理器"""
        if db_path:
            self.db_path = db_path
        else:
            # 使用 config.py 的 get_db_path 方法
            self.db_path = Config.get_db_path(__file__)
            
        # 檢查資料庫是否存在，如果不存在則初始化
        if not os.path.exists(self.db_path):
            self._init_database()
            
    def _init_database(self):
        """初始化資料庫（內部方法）"""
        print(f"🔄 資料庫不存在，正在初始化: {self.db_path}")
        
        # 確保 data 目錄存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 讀取 schema 檔案
        schema_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'schema.sql')
        
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
        except FileNotFoundError:
            print(f"❌ Schema 檔案不存在: {schema_file}")
            print("💡 請先執行: uv run data/init_db.py")
            raise FileNotFoundError(f"Schema 檔案不存在: {schema_file}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 執行 schema SQL
            cursor.executescript(schema_sql)
            conn.commit()
            
        print(f"✅ 資料庫初始化完成: {self.db_path}")
            
    def save_sensor_reading(self, data: Dict[str, Any]) -> bool:
        """儲存感測器讀數"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sensor_readings (temp, humidity, timestamp)
                    VALUES (?, ?, ?)
                ''', (
                    data.get('temp', 0),
                    data.get('humidity', 0),
                    data.get('timestamp', '')
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ 儲存感測器讀數失敗: {e}")
            return False
            
    def save_alert(self, alert_data: Dict[str, Any]) -> bool:
        """儲存警報記錄"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alert_history 
                    (alert_type, severity, message, sensor_data, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    alert_data.get('alert_type', ''),
                    alert_data.get('severity', ''),
                    alert_data.get('message', ''),
                    json.dumps(alert_data.get('sensor_data', {})),
                    alert_data.get('timestamp', '')
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ 儲存警報記錄失敗: {e}")
            return False
            
    def get_recent_readings(self, limit: int = 100) -> list:
        """取得最近的感測器讀數"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT temp, humidity, timestamp, created_at
                    FROM sensor_readings
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ 查詢感測器讀數失敗: {e}")
            return []
            
    def get_recent_alerts(self, limit: int = 50) -> list:
        """取得最近的警報記錄"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT alert_type, severity, message, timestamp, created_at
                    FROM alert_history
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ 查詢警報記錄失敗: {e}")
            return []
            
    def get_statistics(self) -> Dict[str, Any]:
        """取得統計資訊"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 感測器讀數統計
                cursor.execute('SELECT COUNT(*) FROM sensor_readings')
                total_readings = cursor.fetchone()[0]
                
                # 警報統計
                cursor.execute('SELECT COUNT(*) FROM alert_history')
                total_alerts = cursor.fetchone()[0]
                
                # 今日讀數
                cursor.execute('''
                    SELECT COUNT(*) FROM sensor_readings 
                    WHERE DATE(created_at) = DATE('now')
                ''')
                today_readings = cursor.fetchone()[0]
                
                # 今日警報
                cursor.execute('''
                    SELECT COUNT(*) FROM alert_history 
                    WHERE DATE(created_at) = DATE('now')
                ''')
                today_alerts = cursor.fetchone()[0]
                
                return {
                    'total_readings': total_readings,
                    'total_alerts': total_alerts,
                    'today_readings': today_readings,
                    'today_alerts': today_alerts
                }
        except Exception as e:
            print(f"❌ 查詢統計資訊失敗: {e}")
            return {
                'total_readings': 0,
                'total_alerts': 0,
                'today_readings': 0,
                'today_alerts': 0
            }
            
    def cleanup_old_data(self, days: int = 30):
        """清理舊數據（保留指定天數）"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 清理舊的感測器讀數
                cursor.execute('''
                    DELETE FROM sensor_readings 
                    WHERE created_at < datetime('now', '-{} days')
                '''.format(days))
                readings_deleted = cursor.rowcount
                
                # 清理舊的警報記錄
                cursor.execute('''
                    DELETE FROM alert_history 
                    WHERE created_at < datetime('now', '-{} days')
                '''.format(days))
                alerts_deleted = cursor.rowcount
                
                conn.commit()
                print(f"🧹 清理完成: 刪除 {readings_deleted} 筆讀數, {alerts_deleted} 筆警報")
                
        except Exception as e:
            print(f"❌ 清理舊數據失敗: {e}")

if __name__ == "__main__":
    # 測試資料庫功能
    print("🔧 資料庫路徑配置:")
    print(f"   環境變數 DB_PATH: {os.getenv('DB_PATH', '未設定')}")
    print(f"   預設路徑: {Config.DB_PATH}")
    print(f"   實際資料庫路徑: {Config.get_db_path(__file__)}")
    print()
    
    # 展示路徑轉換過程
    print("📋 路徑轉換過程:")
    relative_path = Config.DB_PATH
    final_path = Config.get_db_path(__file__)
    
    print(f"   1. 環境變數: {relative_path}")
    print(f"   2. 最終路徑: {final_path}")
    print(f"   3. 是否為絕對路徑: {os.path.isabs(final_path)}")
    print()
    
    db = DatabaseManager()
    
    # 測試儲存感測器讀數
    test_data = {
        'temp': 25.5,
        'humidity': 60.0,
        'timestamp': datetime.utcnow().isoformat() + "Z"
    }
    
    if db.save_sensor_reading(test_data):
        print("✅ 測試儲存感測器讀數成功")
    
    # 測試儲存警報
    test_alert = {
        'alert_type': 'high_temperature',
        'severity': 'warning',
        'message': '測試高溫警報',
        'sensor_data': test_data,
        'timestamp': datetime.utcnow().isoformat() + "Z"
    }
    
    if db.save_alert(test_alert):
        print("✅ 測試儲存警報成功")
    
    # 顯示統計資訊
    stats = db.get_statistics()
    print(f"📊 統計資訊: {stats}") 