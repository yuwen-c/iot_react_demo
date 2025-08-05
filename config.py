#!/usr/bin/env python3
"""
專案配置檔案
管理所有環境變數和配置設定
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 載入 .env 檔案
def load_env_file():
    """載入 .env 檔案"""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print(f"📋 載入 .env 檔案: {env_file}")
        load_dotenv(env_file)
        # 印出載入的環境變數（可選）
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    print(f"   {key}={value}")
    else:
        print(f"⚠️ .env 檔案不存在: {env_file}")

# 載入 .env 檔案
load_env_file()

class Config:
    """專案配置類別"""
    
    # 資料庫配置
    DB_PATH = os.getenv('DB_PATH', 'data/environment.db')
    
    # MQTT 配置
    MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
    MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
    MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'env/room01/reading')
    
    # Web Server 配置
    WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST', 'localhost')
    WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT', 8000))
    WEB_SERVER_URL = os.getenv('WEB_SERVER_URL', 'http://localhost:8000')
    
    # 警報閾值
    TEMP_THRESHOLD = float(os.getenv('TEMP_THRESHOLD', 30.0))
    HUMIDITY_THRESHOLD = float(os.getenv('HUMIDITY_THRESHOLD', 40.0))
    
    @classmethod
    def get_project_root(cls) -> str:
        """取得專案根目錄"""
        return os.path.dirname(os.path.abspath(__file__))
    
    @classmethod
    def get_db_path(cls, relative_to: Optional[str] = None) -> str:
        """取得資料庫絕對路徑"""
        db_path = cls.DB_PATH
        
        # 如果是相對路徑，轉換為絕對路徑
        if not os.path.isabs(db_path):
            # 總是基於專案根目錄
            project_root = cls.get_project_root()
            db_path = os.path.join(project_root, db_path)
            
        return db_path
    
    @classmethod
    def print_config(cls):
        """印出當前配置"""
        print("📋 專案配置:")
        print(f"   專案根目錄: {cls.get_project_root()}")
        print(f"   資料庫路徑: {cls.DB_PATH}")
        print(f"   完整資料庫路徑: {cls.get_db_path()}")
        print(f"   MQTT Broker: {cls.MQTT_BROKER}:{cls.MQTT_PORT}")
        print(f"   MQTT Topic: {cls.MQTT_TOPIC}")
        print(f"   Web Server: {cls.WEB_SERVER_URL}")
        print(f"   溫度閾值: {cls.TEMP_THRESHOLD}°C")
        print(f"   濕度閾值: {cls.HUMIDITY_THRESHOLD}%")

if __name__ == "__main__":
    Config.print_config() 