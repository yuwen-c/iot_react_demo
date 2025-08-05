第一階段：基礎 MQTT 通訊建立

設置 MQTT Broker (Mosquitto)
建立 mosquitto/ 目錄和配置
使用 Docker 啟動 Mosquitto
測試 Broker 是否正常運作
開發 sensor.py
實現模擬感測器數據生成
建立 MQTT 發布功能
測試數據是否能正確發布到 Broker
開發 controller.py
實現 MQTT 訂閱功能
測試是否能接收 sensor.py 的數據
實現基本的警報判斷邏輯

第二階段：數據持久化與共享資料庫

建立 data/ 目錄存放共享資料庫
建立 controller/database.py 模組
設計資料表結構 (sensor_readings, alert_history)
實現數據儲存功能
測試數據持久化是否正常
建立 server/database.py 模組
實現數據查詢功能
測試 Web Server 是否能讀取共享資料庫

第三階段：HTTP 警報通知機制

開發 FastAPI Server
建立基本的 REST API
實現 /api/alerts endpoint 接收 HTTP 警報通知
修改 controller.py 加入 HTTP 通知功能
測試 controller.py 到 FastAPI 的警報通知
實現 WebSocket 連接
測試 WebSocket 即時推播功能

第四階段：前端開發

開發 React 前端
建立基本頁面結構
實現 WebSocket 連接接收警報
開發即時數據圖表
實現歷史數據查詢功能

第五階段：整合測試

端到端測試
測試完整數據流：Sensor → MQTT → Controller → HTTP → Server → WebSocket → Frontend
優化性能和穩定性
部署和監控