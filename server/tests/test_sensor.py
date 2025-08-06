#!/usr/bin/env python3
"""
感測器 API 端點測試
測試所有感測器相關的 API 功能
"""

import pytest
from datetime import datetime, timedelta

# 測試最新讀數端點
@pytest.mark.asyncio
async def test_get_latest_sensor_reading(async_client):
    """測試取得最新感測器讀數"""
    response = await async_client.get("/api/sensor/latest")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    
    reading = data["data"]
    assert "id" in reading
    assert "temp" in reading
    assert "humidity" in reading
    assert "timestamp" in reading
    assert "created_at" in reading

# 測試讀數列表端點
@pytest.mark.asyncio
async def test_get_sensor_readings(async_client):
    """測試取得感測器讀數列表"""
    # 測試預設參數
    response = await async_client.get("/api/sensor/readings")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) <= 100  # 預設限制

    # 測試自訂限制和偏移
    response = await async_client.get("/api/sensor/readings?limit=5&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) <= 5
    assert data["limit"] == 5
    assert data["offset"] == 2

    # 測試無效參數
    response = await async_client.get("/api/sensor/readings?limit=0")
    assert response.status_code == 422  # FastAPI 的驗證錯誤

# 測試日期範圍查詢端點
@pytest.mark.asyncio
async def test_get_sensor_readings_by_date_range(async_client):
    """測試根據日期範圍取得感測器讀數"""
    # 取得今天和昨天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 測試有效日期範圍
    response = await async_client.get(
        f"/api/sensor/readings/range?start_date={yesterday}&end_date={today}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "count" in data
    
    # 測試無效日期格式
    response = await async_client.get(
        "/api/sensor/readings/range?start_date=invalid&end_date=2025-01-01"
    )
    assert response.status_code == 500

# 測試統計資訊端點
@pytest.mark.asyncio
async def test_get_sensor_statistics(async_client):
    """測試取得感測器統計資訊"""
    response = await async_client.get("/api/sensor/statistics")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    
    stats = data["data"]
    required_fields = [
        "total_readings",
        "avg_temp",
        "avg_humidity",
        "min_temp",
        "max_temp",
        "min_humidity",
        "max_humidity",
        "latest_reading_time"
    ]
    
    for field in required_fields:
        assert field in stats

# 測試錯誤處理
@pytest.mark.asyncio
async def test_error_handling(async_client):
    """測試錯誤處理情況"""
    # 測試無效的日期範圍
    response = await async_client.get(
        "/api/sensor/readings/range?start_date=2025-01-01&end_date=2024-01-01"
    )
    assert response.status_code == 500

    # 測試無效的限制值
    response = await async_client.get("/api/sensor/readings?limit=1001")
    assert response.status_code == 422  # FastAPI 的驗證錯誤