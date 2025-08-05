iot-react-demo/
├── docker-compose.yml        # 管理整體服務
├── .env                      # 全域環境變數（如 MQTT host）
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
│   │   └── alerts.py         # 警報歷史查詢 API
│   ├── database.py           # SQLite 資料庫查詢模組
│   ├── static/               # 放 React build 後靜態檔案
│   ├── requirements.txt
│   └── Dockerfile
├── data/
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

- **sensor.py**: 模擬感測器，發布 MQTT 數據
- **controller.py**: MQTT 訂閱、警報判斷、數據寫入、HTTP 通知
- **server/main.py**: 接收 HTTP 警報、WebSocket 推播、REST API、數據查詢
- **data/environment.db**: 共享資料庫，支援多進程讀寫
- **React Frontend**: 即時數據顯示、警報接收、歷史查詢
