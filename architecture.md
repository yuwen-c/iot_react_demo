iot-react-demo/
├── docker-compose.yml        # 管理整體服務
├── .env                      # 全域環境變數（如 MQTT host）
├── config.py                 # 專案配置管理
├── mosquitto/
│   ├── config/
│   │   └── mosquitto.conf    # MQTT broker 設定
│   └── Dockerfile            # 可選，自訂 Mosquitto 映像
├── sensor/
│   ├── sensor.py             # Python 模擬感測器發 MQTT
│   ├── requirements.txt      # Python 依賴清單
│   └── Dockerfile
├── controller/
│   ├── controller.py         # Python 訂閱 MQTT + 判斷警報 + 數據寫入 + HTTP 通知
│   ├── requirements.txt
│   ├── database.py           # SQLite 資料庫寫入模組
│   └── Dockerfile
├── server/
│   ├── main.py               # FastAPI + WebSocket server 主程式
│   ├── api/                  # REST API 路由
│   │   ├── __init__.py
│   │   ├── sensor_data.py    # 感測數據查詢 API
│   │   └── alerts.py         # 警報歷史查詢與通知 API
│   ├── core/                 # 核心基礎設施
│   │   ├── __init__.py
│   │   ├── database.py       # 資料庫管理模組
│   │   └── websocket.py         # WebSocket 連線管理
│   ├── static/               # 放 React build 後靜態檔案
│   ├── requirements.txt
│   └── Dockerfile
├── data/                     # 資料庫管理目錄
│   ├── schema.sql            # 資料庫 Schema 定義
│   ├── init_db.py            # 資料庫初始化腳本
│   └── environment.db        # 共享 SQLite 資料庫檔案
├── frontend/                 # React 應用（可選容器）
│   ├── src/
│   │   ├── components/
│   │   │   ├── RealTimeChart.jsx    # 即時數據圖表
│   │   │   ├── AlertHistory.jsx     # 警報歷史組件
│   │   │   └── DataTable.jsx        # 歷史數據表格
│   │   ├── services/
│   │   │   └── api.js               # API 調用服務
│   │   └── App.jsx
│   ├── public/
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile            # 若也要容器化 React

## 架構流程圖

```
[sensor.py] ──(MQTT)──▶ [MQTT broker] ──▶ [controller.py]
                                              ├─ 儲存數據到資料庫 (SQLite)
                                              └─ 發 HTTP 通知 → [FastAPI server]
                                                                  ├─ 推播警報 (WebSocket)
                                                                  └─ 提供歷史 API → [React 前端]
```

```
          +---------------------+
          |     sensor.py       | ← 模擬資料，每 5 秒發送 MQTT
          +----------+----------+
                     |
                     ▼
             +--------------+      +-----------------------+
             |  Mosquitto   | ◀──▶ |     controller.py      |
             |   (Broker)   |      | 訂閱 MQTT、判斷警報邏輯  |
             +------+-------+      | 數據寫入、HTTP 通知      |
                    |              +-----------+-----------+
                    |                          |
                    |                          ▼
                    |              +----------------------+
                    |              |   data/environment.db |
                    |              |   (共享 SQLite 資料庫) |
                    |              +----------+-----------+
                    |                         |
                    |                         ▼
                    |              +----------------------+
                    |              |     server/main.py    |
                    |              | FastAPI + WebSocket   |
                    |              | 接收 HTTP 警報通知     |
                    |              +----------+-----------+
                    |                         |
                    |                         ▼
                    |              +----------------------+
                    |              |    React Frontend    |
                    |              | 即時圖表 + 警報顯示   |
                    |              +----------------------+
                    |
                    ▼
            +----------------+
            |   Web Server   |
            | (FastAPI + ws) |
            |  提供 React App |
            +-------+--------+
                    |
                    ▼
        [React 前端 SPA 應用 (e.g. Vite)]
        - 顯示即時圖表（Chart.js/Recharts）
        - 接收 WebSocket 警報
        - 查詢歷史數據 API
```

## 數據流向

1. **sensor.py** → MQTT Broker → **controller.py**
2. **controller.py** → 寫入 **data/environment.db**
3. **controller.py** → HTTP POST → **server/main.py**
4. **server/main.py** → WebSocket → **React Frontend**
5. **server/main.py** → 查詢 **data/environment.db** → REST API → **React Frontend**

## 職責分離

### **核心服務**
- **sensor.py**: 模擬感測器，發布 MQTT 數據
- **controller.py**: MQTT 訂閱、警報判斷、數據寫入、HTTP 通知
- **server/main.py**: 接收 HTTP 警報、WebSocket 推播、REST API、數據查詢
- **React Frontend**: 即時數據顯示、警報接收、歷史查詢

### **核心基礎設施**
- **server/core/database.py**: 資料庫管理（查詢操作、連線管理）
- **server/core/websocket.py**: WebSocket 連線管理與推播

### **資料庫管理**
- **data/schema.sql**: 資料庫 Schema 定義（感測器讀數表、警報歷史表）
- **data/init_db.py**: 資料庫初始化腳本（建立資料表、索引）
- **data/environment.db**: 共享 SQLite 資料庫檔案
- **controller/database.py**: 資料庫寫入操作（儲存感測數據、警報記錄）

### **配置管理**
- **config.py**: 專案配置管理（資料庫路徑、MQTT 設定、警報閾值）
- **.env**: 環境變數配置（可選，用於自訂設定）

## 資料庫初始化流程

### **手動初始化**
```bash
# 1. 初始化資料庫
uv run data/init_db.py

# 2. 啟動 controller
uv run controller/controller.py
```

### **自動初始化**
- 如果資料庫不存在，`controller/database.py` 會自動初始化
- 如果 schema 檔案不存在，會提示執行 `data/init_db.py`

### **Schema 管理**
- 所有資料表定義集中在 `data/schema.sql`
- 支援資料庫遷移和版本管理
- 包含索引定義以提升查詢效能

## 開發流程

### **1. 環境設置**
```bash
# 安裝依賴
uv sync

# 初始化資料庫
uv run data/init_db.py
```

### **2. 啟動服務**
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

### **3. 測試流程**
- 感測器數據 → MQTT → 控制器 → 資料庫
- 警報判斷 → HTTP 通知 → 伺服器 → WebSocket → 前端
- 歷史查詢 → 伺服器 → 資料庫 → REST API → 前端
