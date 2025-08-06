#!/usr/bin/env python3
"""
Pytest 配置檔案
提供共用的測試配置和 fixtures
"""

import sys
import os
import pytest
import pytest_asyncio
import asyncio
import httpx
from httpx import AsyncClient

# 將專案根目錄加入 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from server.main import app
from config import Config

# 測試配置
BASE_URL = f"http://{Config.WEB_SERVER_HOST}:{Config.WEB_SERVER_PORT}"

@pytest_asyncio.fixture
async def async_client():
    """提供異步 HTTP 客戶端"""
    async with AsyncClient(
        base_url="http://test",
        transport=httpx.ASGITransport(app=app)
    ) as client:
        yield client

@pytest.fixture
def event_loop():
    """提供事件循環"""
    loop = asyncio.get_event_loop()
    yield loop