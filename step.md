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

第二階段：數據持久化

建立 SQLite 資料庫
設計資料表結構 (sensor_readings, alert_history)
實現數據儲存功能
測試數據持久化是否正常

第三階段：WebSocket 即時通訊

開發 FastAPI Server
建立基本的 REST API
實現 WebSocket 連接
測試 controller.py 到 FastAPI 的警報推播

第四階段：前端開發

開發 React 前端
建立基本頁面結構
實現 WebSocket 連接接收警報
開發即時數據圖表
實現歷史數據查詢功能

第五階段：整合測試

端到端測試
測試完整數據流
優化性能和穩定性
部署和監控