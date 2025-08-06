#!/usr/bin/env python3
"""
FastAPI Web Server 主程式
提供 REST API 和 WebSocket 服務
"""

import sys
import os

# 將專案根目錄加入 Python 路徑，以便導入 config
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from config import Config

# 建立 FastAPI 應用程式
app = FastAPI(
    title="IoT 環境監控系統",
    description="室內環境監控與警報系統的 Web Server",
    version="1.0.0"
)

# 設定 CORS（允許前端存取）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React 開發伺服器
        "http://localhost:5173",  # Vite 開發伺服器
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基本測試端點
@app.get("/")
async def root():
    """根路徑測試端點"""
    return {
        "message": "IoT 環境監控系統 Web Server",
        "status": "running 🏃",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "database_path": Config.get_db_path(),
        "web_server_url": Config.WEB_SERVER_URL
    }

@app.get("/api/config")
async def get_config():
    """取得系統配置資訊"""
    return {
        "database_path": Config.DB_PATH,
        "mqtt_broker": f"{Config.MQTT_BROKER}:{Config.MQTT_PORT}",
        "mqtt_topic": Config.MQTT_TOPIC,
        "web_server_url": Config.WEB_SERVER_URL,
        "temp_threshold": Config.TEMP_THRESHOLD,
        "humidity_threshold": Config.HUMIDITY_THRESHOLD
    }

# 啟動伺服器
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload