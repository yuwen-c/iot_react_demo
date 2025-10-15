# 測試說明

本目錄包含所有的單元測試和整合測試。

## 📦 測試環境設置

### 安裝測試依賴

```bash
# 使用 uv 安裝測試相關套件
uv add --dev pytest pytest-asyncio httpx websockets
```

## 🧪 執行測試

### 執行所有測試

```bash
# 在專案根目錄執行
uv run pytest server/tests/ -v

# 或在 server 目錄執行
cd server
uv run pytest tests/ -v
```

### 執行特定測試檔案

```bash
# 測試基本 API 端點
uv run pytest server/tests/test_main.py -v

# 測試感測器 API
uv run pytest server/tests/test_sensor.py -v

# 測試警報歷史 API
uv run pytest server/tests/test_alert_history.py -v

# 測試警報通知和推播
uv run pytest server/tests/test_alert_notification.py -v

# 測試 WebSocket 功能
uv run pytest server/tests/test_websocket.py -v
```

### 執行特定測試函數

```bash
# 執行特定測試函數
uv run pytest server/tests/test_websocket.py::test_websocket_connection -v

# 執行包含關鍵字的測試
uv run pytest server/tests/ -k "websocket" -v
```

### 顯示詳細輸出

```bash
# 顯示 print 輸出
uv run pytest server/tests/ -v -s

# 顯示更詳細的錯誤訊息
uv run pytest server/tests/ -v --tb=long
```

## 🚀 手動測試

除了自動化測試外，還有一個獨立的手動測試腳本：

```bash
# 執行手動測試（需要先啟動 Web Server）
uv run python server/test_main.py
```

這個腳本會測試：
- ✅ 基本 API 端點
- ✅ 健康檢查
- ✅ 配置資訊
- ✅ API 文檔
- ✅ WebSocket 連線
- ✅ WebSocket 警報推播

## 📋 測試檔案說明

| 檔案 | 說明 |
|------|------|
| `conftest.py` | pytest 配置檔案，提供共用的 fixtures |
| `test_main.py` | 基本 API 端點測試 |
| `test_sensor.py` | 感測器資料 API 測試 |
| `test_alert_history.py` | 警報歷史查詢 API 測試 |
| `test_alert_notification.py` | 警報通知與推播測試 |
| `test_websocket.py` | WebSocket 連線與推播測試 |

## 🔍 WebSocket 測試內容

`test_websocket.py` 包含以下測試：

1. **test_websocket_connection** - 測試 WebSocket 連線建立與關閉
2. **test_websocket_alert_broadcast** - 測試警報透過 WebSocket 推播
3. **test_multiple_websocket_connections** - 測試多個 WebSocket 連線同時接收推播
4. **test_websocket_with_different_alert_types** - 測試不同類型的警報推播
5. **test_websocket_reconnection** - 測試 WebSocket 重新連線
6. **test_websocket_without_broadcast** - 測試 WebSocket 空閒狀態

## ⚙️ 測試前準備

### 1. 啟動 Web Server（用於手動測試）

```bash
cd server
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 執行測試

```bash
# 在另一個終端執行
uv run pytest server/tests/ -v
```

## 📊 測試覆蓋率

如果需要查看測試覆蓋率：

```bash
# 安裝 pytest-cov
uv add --dev pytest-cov

# 執行測試並生成覆蓋率報告
uv run pytest server/tests/ --cov=server --cov-report=html

# 查看報告（會生成在 htmlcov/ 目錄）
open htmlcov/index.html
```

## 🐛 常見問題

### 測試失敗：連線被拒絕

```
ConnectionRefusedError: [Errno 61] Connect call failed
```

**解決方法**：確保 Web Server 正在運行。

### WebSocket 測試超時

```
TimeoutError: waiting for WebSocket message
```

**解決方法**：檢查 WebSocket 推播功能是否正常，確認 `alerts.py` 中的推播代碼已正確實作。

### 資料庫相關錯誤

**解決方法**：確保測試資料庫存在且可訪問。

## 💡 提示

- 使用 `-v` 參數可以看到更詳細的測試輸出
- 使用 `-s` 參數可以看到測試中的 print 輸出
- 使用 `-x` 參數可以在第一個失敗時停止測試
- 使用 `-k` 參數可以只執行名稱包含特定關鍵字的測試

