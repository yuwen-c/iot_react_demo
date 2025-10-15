#!/usr/bin/env python3
"""
WebSocket 功能測試
測試 WebSocket 連線、推播和錯誤處理
"""

import pytest
import asyncio
from datetime import datetime
from fastapi import WebSocketDisconnect

@pytest.mark.asyncio
async def test_websocket_connection(websocket_client):
    """測試 WebSocket 連線建立與關閉"""
    with websocket_client.websocket_connect("/ws/alerts") as websocket:
        # 驗證連線成功
        assert websocket is not None
        print("✅ WebSocket 連線建立成功")

@pytest.mark.asyncio
async def test_websocket_alert_broadcast(async_client, websocket_client):
    """測試警報透過 WebSocket 推播"""
    with websocket_client.websocket_connect("/ws/alerts") as websocket:
        # 準備警報資料
        alert_data = {
            "alert_type": "high_temperature",
            "severity": "warning",
            "message": "高溫警報測試",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_data": {
                "temp": 31.5,
                "humidity": 50.0,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # 發送警報通知
        response = await async_client.post("/api/alerts/notify", json=alert_data)
        assert response.status_code == 200
        
        # 接收 WebSocket 推播
        data = websocket.receive_json()
        
        # 驗證推播資料結構
        assert "type" in data
        assert data["type"] == "alert"
        assert "data" in data
        assert "broadcast_time" in data
        
        # 驗證推播內容
        alert = data["data"]
        assert alert["alert_type"] == "high_temperature"
        assert alert["severity"] == "warning"
        assert alert["message"] == "高溫警報測試"
        assert "sensor_data" in alert
        
        print("✅ WebSocket 推播測試通過")

@pytest.mark.asyncio
async def test_multiple_websocket_connections(async_client, websocket_client):
    """測試多個 WebSocket 連線同時接收推播"""
    # 建立多個 WebSocket 連線
    with websocket_client.websocket_connect("/ws/alerts") as ws1, \
         websocket_client.websocket_connect("/ws/alerts") as ws2, \
         websocket_client.websocket_connect("/ws/alerts") as ws3:
        
        # 發送警報通知
        alert_data = {
            "alert_type": "low_humidity",
            "severity": "info",
            "message": "低濕度警報測試",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_data": {
                "temp": 25.0,
                "humidity": 29.0,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        response = await async_client.post("/api/alerts/notify", json=alert_data)
        assert response.status_code == 200
        
        # 驗證所有連線都收到推播
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()
        data3 = ws3.receive_json()
        
        assert data1["type"] == "alert"
        assert data2["type"] == "alert"
        assert data3["type"] == "alert"
        
        assert data1["data"]["message"] == "低濕度警報測試"
        assert data2["data"]["message"] == "低濕度警報測試"
        assert data3["data"]["message"] == "低濕度警報測試"
        
        print("✅ 多連線推播測試通過")

@pytest.mark.asyncio
async def test_websocket_with_different_alert_types(async_client, websocket_client):
    """測試不同類型的警報推播"""
    with websocket_client.websocket_connect("/ws/alerts") as websocket:
        # 測試高溫警報
        high_temp_alert = {
            "alert_type": "high_temperature",
            "severity": "error",
            "message": "高溫緊急警報",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_data": {"temp": 35.0, "humidity": 40.0}
        }
        
        await async_client.post("/api/alerts/notify", json=high_temp_alert)
        data1 = websocket.receive_json()
        assert data1["data"]["alert_type"] == "high_temperature"
        assert data1["data"]["severity"] == "error"
        
        # 測試低濕度警報
        low_humidity_alert = {
            "alert_type": "low_humidity",
            "severity": "warning",
            "message": "低濕度警報",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_data": {"temp": 25.0, "humidity": 25.0}
        }
        
        await async_client.post("/api/alerts/notify", json=low_humidity_alert)
        data2 = websocket.receive_json()
        assert data2["data"]["alert_type"] == "low_humidity"
        assert data2["data"]["severity"] == "warning"
        
        print("✅ 不同警報類型測試通過")

@pytest.mark.asyncio
async def test_websocket_reconnection(websocket_client):
    """測試 WebSocket 重新連線"""
    # 第一次連線
    with websocket_client.websocket_connect("/ws/alerts") as ws1:
        assert ws1 is not None
    
    # 重新連線
    with websocket_client.websocket_connect("/ws/alerts") as ws2:
        assert ws2 is not None
    
    print("✅ WebSocket 重新連線測試通過")

@pytest.mark.asyncio
async def test_websocket_without_broadcast(websocket_client):
    """測試 WebSocket 連線但無推播時的狀態"""
    with websocket_client.websocket_connect("/ws/alerts") as websocket:
        # 只是建立連線，不發送任何警報
        # 連線應該保持開啟狀態
        assert websocket is not None
        print("✅ WebSocket 空閒狀態測試通過")

