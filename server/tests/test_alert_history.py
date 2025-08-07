#!/usr/bin/env python3
"""
警報歷史 API 端點測試
測試所有警報歷史相關的 API 功能
"""

import pytest
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_get_alert_history(async_client):
    """測試取得警報歷史列表"""
    # 測試預設參數
    response = await async_client.get("/api/alerts/history")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # 檢查回傳資料結構
    if len(data["data"]) > 0:
        alert = data["data"][0]
        required_fields = [
            "id",
            "alert_type",
            "severity",
            "message",
            "sensor_data",
            "timestamp",
            "sent_to_frontend",
            "created_at"
        ]
        for field in required_fields:
            assert field in alert

@pytest.mark.asyncio
async def test_get_alert_history_with_filters(async_client):
    """測試使用過濾條件取得警報歷史"""
    # 測試警報類型過濾
    response = await async_client.get("/api/alerts/history?alert_type=temperature")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    if len(data["data"]) > 0:
        assert all(alert["alert_type"] == "temperature" for alert in data["data"])

    # 測試嚴重程度過濾
    response = await async_client.get("/api/alerts/history?severity=warning")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    if len(data["data"]) > 0:
        assert all(alert["severity"] == "warning" for alert in data["data"])

@pytest.mark.asyncio
async def test_get_alert_history_with_date_range(async_client):
    """測試使用日期範圍取得警報歷史"""
    # 取得今天和昨天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    response = await async_client.get(
        f"/api/alerts/history/range?start_date={yesterday}&end_date={today}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "count" in data

@pytest.mark.asyncio
async def test_get_alert_statistics(async_client):
    """測試取得警報統計資訊"""
    response = await async_client.get("/api/alerts/statistics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    
    stats = data["data"]
    required_fields = [
        "total_alerts",
        "alerts_by_type",
        "alerts_by_severity",
        "alerts_last_24h",
        "latest_alert_time"
    ]
    for field in required_fields:
        assert field in stats

@pytest.mark.asyncio
async def test_get_alert_history_pagination(async_client):
    """測試警報歷史分頁功能"""
    # 測試限制筆數
    response = await async_client.get("/api/alerts/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) <= 5

    # 測試偏移量
    response = await async_client.get("/api/alerts/history?offset=2&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "limit" in data
    assert "offset" in data
    assert data["limit"] == 5
    assert data["offset"] == 2

@pytest.mark.asyncio
async def test_error_handling(async_client):
    """測試錯誤處理情況"""
    # 測試無效的日期範圍
    response = await async_client.get(
        "/api/alerts/history/range?start_date=2025-01-01&end_date=2024-01-01"
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    error_data = data["detail"]
    assert error_data["status"] == "error"
    assert "message" in error_data

    # 測試無效的限制值
    response = await async_client.get("/api/alerts/history?limit=1001")
    assert response.status_code == 422  # FastAPI 的驗證錯誤

    # 測試無效的警報類型
    response = await async_client.get("/api/alerts/history?alert_type=invalid_type")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    error_data = data["detail"]
    assert error_data["status"] == "error"
    assert "message" in error_data
