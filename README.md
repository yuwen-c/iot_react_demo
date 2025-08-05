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
├── sensor/          # 感測器模擬
├── controller/      # MQTT 控制器 + 數據寫入
├── server/          # FastAPI 伺服器 + 數據查詢
├── frontend/        # React 前端
├── mosquitto/       # MQTT 配置
├── data/            # 共享資料庫檔案
├── pyproject.toml   # Python 依賴管理 (uv)
└── .venv/           # Python 虛擬環境
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

### 4. 測試流程
```bash
# 終端 1: 啟動 MQTT Broker
cd mosquitto && ./start_local.sh

# 終端 2: 啟動感測器
uv run sensor/sensor.py

# 終端 3: 啟動控制器
uv run controller/controller.py

# 終端 4: 啟動伺服器
uv run server/main.py

# 終端 5: 啟動前端
cd frontend && npm run dev
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