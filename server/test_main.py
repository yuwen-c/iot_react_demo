#!/usr/bin/env python3
"""
FastAPI 基本功能測試
測試 API 端點是否正常運作
"""

import sys
import os
import asyncio
import httpx
import json

# 將專案根目錄加入 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import Config

# 測試配置
BASE_URL = f"http://{Config.WEB_SERVER_HOST}:{Config.WEB_SERVER_PORT}"

async def test_root_endpoint():
    """測試根路徑端點"""
    print("🧪 測試根路徑端點...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {response.json()}")
        return response.status_code == 200

async def test_health_endpoint():
    """測試健康檢查端點"""
    print("\n🧪 測試健康檢查端點...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/health")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {response.json()}")
        return response.status_code == 200

async def test_config_endpoint():
    """測試配置端點"""
    print("\n🧪 測試配置端點...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/config")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200

async def test_docs_endpoint():
    """測試 API 文檔端點"""
    print("\n🧪 測試 API 文檔端點...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/docs")
        print(f"   狀態碼: {response.status_code}")
        print(f"   API 文檔可存取: {response.status_code == 200}")
        return response.status_code == 200

async def run_all_tests():
    """執行所有測試"""
    print("🚀 開始 FastAPI 功能測試...")
    print(f"   測試目標: {BASE_URL}")
    
    tests = [
        ("根路徑", test_root_endpoint),
        ("健康檢查", test_health_endpoint),
        ("配置資訊", test_config_endpoint),
        ("API 文檔", test_docs_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
            status = "✅ 通過" if result else "❌ 失敗"
            print(f"   {test_name}: {status}")
        except Exception as e:
            print(f"   {test_name}: ❌ 錯誤 - {e}")
            results.append((test_name, False))
    
    # 總結
    print("\n📊 測試結果總結:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 總計: {passed}/{total} 個測試通過")
    
    if passed == total:
        print("🎉 所有測試都通過了！FastAPI 伺服器運作正常。")
    else:
        print("⚠️ 部分測試失敗，請檢查伺服器狀態。")

if __name__ == "__main__":
    # 執行測試
    asyncio.run(run_all_tests()) 