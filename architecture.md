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
│   ├── controller.py         # Python 訂閱 + 判斷 + 數據持久化 + WebSocket 推播
│   ├── requirements.txt
│   ├── database.py           # SQLite 資料庫管理模組
│   ├── iot_data.db          # SQLite 資料庫檔案（自動生成）
│   └── Dockerfile
├── server/
│   ├── main.py               # FastAPI + WebSocket server 主程式
│   ├── api/                  # REST API 路由
│   │   ├── __init__.py
│   │   ├── sensor_data.py    # 感測數據查詢 API
│   │   └── alerts.py         # 警報歷史查詢 API
│   ├── static/               # 放 React build 後靜態檔案
│   ├── requirements.txt
│   └── Dockerfile
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
