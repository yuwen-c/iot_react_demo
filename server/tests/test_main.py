#!/usr/bin/env python3
"""
基本 API 端點測試
測試基礎端點的功能
"""

import json
import pytest

@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    """測試根路徑端點"""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert "version" in data

@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    """測試健康檢查端點"""
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database_path" in data
    assert "web_server_url" in data

@pytest.mark.asyncio
async def test_config_endpoint(async_client):
    """測試配置端點"""
    response = await async_client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    required_fields = [
        "database_path",
        "mqtt_broker",
        "mqtt_topic",
        "web_server_url",
        "temp_threshold",
        "humidity_threshold"
    ]
    for field in required_fields:
        assert field in data

@pytest.mark.asyncio
async def test_docs_endpoint(async_client):
    """測試 API 文檔端點"""
    response = await async_client.get("/docs")
    assert response.status_code == 200