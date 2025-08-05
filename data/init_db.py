#!/usr/bin/env python3
"""
資料庫初始化腳本
建立資料庫檔案和 schema
"""

import sqlite3
import os
import sys

# 加入專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def get_project_root():
    """取得專案根目錄"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """初始化資料庫"""
    # 使用 Config 類別取得資料庫路徑
    db_path = Config.get_db_path()
    
    print(f"🔧 初始化資料庫: {db_path}")
    
    # 確保目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 讀取 schema 檔案
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
    except FileNotFoundError:
        print(f"❌ Schema 檔案不存在: {schema_file}")
        return False
    
    # 建立資料庫連接
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # 執行 schema SQL
            cursor.executescript(schema_sql)
            conn.commit()
            
            print("✅ 資料庫初始化成功")
            
            # 顯示建立的資料表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"📋 建立的資料表: {[table[0] for table in tables]}")
            
            return True
            
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        return False

def check_database():
    """檢查資料庫狀態"""
    # 使用 Config 類別取得資料庫路徑
    db_path = Config.get_db_path()
    
    if not os.path.exists(db_path):
        print(f"❌ 資料庫檔案不存在: {db_path}")
        return False
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # 檢查資料表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            expected_tables = ['sensor_readings', 'alert_history']
            existing_tables = [table[0] for table in tables]
            
            print(f"📋 現有資料表: {existing_tables}")
            
            missing_tables = set(expected_tables) - set(existing_tables)
            if missing_tables:
                print(f"⚠️ 缺少資料表: {missing_tables}")
                return False
            else:
                print("✅ 所有必要資料表都存在")
                return True
                
    except Exception as e:
        print(f"❌ 檢查資料庫失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 資料庫初始化工具")
    print("=" * 50)
    
    # 顯示路徑資訊
    project_root = get_project_root()
    db_path = Config.get_db_path()
    
    print(f"📋 路徑資訊:")
    print(f"   專案根目錄: {project_root}")
    print(f"   環境變數 DB_PATH: {os.getenv('DB_PATH', '未設定')}")
    print(f"   Config.DB_PATH: {Config.DB_PATH}")
    print(f"   完整資料庫路徑: {db_path}")
    print()
    
    # 檢查資料庫狀態
    if check_database():
        print("✅ 資料庫已存在且結構正確")
    else:
        print("🔄 開始初始化資料庫...")
        if init_database():
            print("✅ 資料庫初始化完成")
        else:
            print("❌ 資料庫初始化失敗")
            sys.exit(1) 