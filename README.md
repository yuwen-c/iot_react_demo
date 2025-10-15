# IoT 室內環境監控系統

## 專案概述
本系統模擬室內環境監控場景，即時監測溫度與濕度，並在環境異常時發出警報。

## 開發環境設置

### 前置需求
- Python 3.11+
- Node.js 16+
- Mosquitto MQTT Broker
- uv (Python 套件管理工具)

### 安裝 uv (如果還沒安裝)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安裝 Mosquitto (macOS)
```bash
brew install mosquitto
brew services start mosquitto
```

### 專案結構
```
iot-react-demo/
├── sensor/          # 感測器模擬，產生並發布溫濕度數據 (publisher)(script)
├── controller/      # 訂閱 MQTT Broker 接收感測器數據 + 數據寫入 + 發送警報 (subscriber)(script)
├── server/          # FastAPI 伺服器 + 數據查詢 (server)
├── frontend/        # React 前端
├── mosquitto/       # MQTT 配置，接收數據並發布，管理連線和訂閱 (broker，server `-d` 背景執行)(server)
├── data/            # 共享資料庫檔案
├── pyproject.toml   # Python 依賴管理 (uv)
└── .venv/           # Python 虛擬環境
```

## 數據流向

```mermaid
sensor.py → MQTT Broker → controller.py → SQLite DB (data/environment.db)
                                    ↓
                            HTTP 通知 → server/main.py
                                           ↓
                                    WebSocket → React 前端
```


## 開發流程

### 1. 設置 Python 環境
```bash
# 安裝所有 Python 依賴
uv sync

# 啟動虛擬環境
source .venv/bin/activate
```

### 2. 啟動 MQTT Broker
```bash
# 檢查 Mosquitto 是否運行
mosquitto_sub -h localhost -t "test" -v
```

### 3. 開發順序
1. **sensor/** - 模擬感測器數據發布
2. **controller/** - MQTT 訂閱、警報判斷、數據寫入、HTTP 通知
3. **server/** - FastAPI 伺服器、接收 HTTP 警報、WebSocket 推播、數據查詢
4. **frontend/** - React 前端應用

### 4. 進入開發環境指令
```bash
# 終端 1: 啟動 MQTT Broker (背景執行)
cd mosquitto && ./start_local.sh

# 終端 2: 啟動感測器(感測器模擬，產生並發布溫濕度數據)
uv run sensor/sensor.py

# 終端 3: 啟動控制器(訂閱 MQTT Broker 接收感測器數據 + 數據寫入 + 發送警報)
uv run controller/controller.py

# 終端 4: 啟動伺服器
# 在專案根目錄執行
uv run uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

# 終端 5: 啟動前端
cd frontend && npm run dev
```

### 5. 跑測試

```bash
# 執行所有測試
uv run pytest server/tests/ -v

# 只執行 WebSocket 測試
uv run pytest server/tests/test_websocket.py -v

```

## 技術棧

- **Python 環境**: uv + 共用虛擬環境
- **MQTT**: Eclipse Mosquitto
- **後端**: Python + FastAPI + SQLite
- **前端**: React + Vite + Chart.js
- **通訊**: WebSocket + MQTT + HTTP

## 共用 Python 依賴

所有 Python 模組共用同一個 uv 環境，依賴定義在 `pyproject.toml`：
- `paho-mqtt` - MQTT 客戶端
- `fastapi` - Web 框架
- `uvicorn` - ASGI 伺服器
- `websockets` - WebSocket 支援
- `requests` - HTTP 客戶端 (controller 通知 server) 