#!/usr/bin/env python3
"""
警報通知 API 端點測試
測試接收來自 Controller 的警報通知並進行 WebSocket 推播
"""

import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_receive_alert_notification(async_client):
    """測試接收正確格式的警報通知"""
    alert_data = {
        "alert_type": "high_temperature",
        "severity": "warning",
        "message": "高溫警報！當前溫度 31°C 超過閾值 30°C",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sensor_data": {
            "temp": 31.0,
            "humidity": 45.0,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }
    
    response = await async_client.post("/api/alerts/notify", json=alert_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "警報通知已接收並推播"

@pytest.mark.asyncio
async def test_invalid_alert_format(async_client):
    """測試接收格式錯誤的警報通知"""
    # 缺少必要欄位
    invalid_data = {
        "alert_type": "high_temperature",
        "message": "測試警報"
    }
    
    response = await async_client.post("/api/alerts/notify", json=invalid_data)
    assert response.status_code == 422  # FastAPI 的驗證錯誤

    # 無效的警報類型
    invalid_type_data = {
        "alert_type": "invalid_type",
        "severity": "warning",
        "message": "測試警報",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sensor_data": {}
    }
    
    response = await async_client.post("/api/alerts/notify", json=invalid_type_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "無效的警報類型" in data["detail"]["message"]

@pytest.mark.asyncio
async def test_alert_websocket_broadcast(async_client, websocket_client):
    """測試警報通知是否正確透過 WebSocket 推播"""
    # 建立 WebSocket 連線
    async with websocket_client.websocket_connect("/ws/alerts") as websocket:
        # 發送警報通知
        alert_data = {
            "alert_type": "high_temperature",
            "severity": "warning",
            "message": "高溫警報！當前溫度 32°C 超過閾值 30°C",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_data": {
                "temp": 32.0,
                "humidity": 45.0,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        response = await async_client.post("/api/alerts/notify", json=alert_data)
        assert response.status_code == 200
        
        # 接收 WebSocket 推播
        data = await websocket.receive_json()
        assert data["type"] == "alert"
        assert data["data"]["alert_type"] == alert_data["alert_type"]
        assert data["data"]["message"] == alert_data["message"]

# 需要在 conftest.py 中新增 websocket_client fixture