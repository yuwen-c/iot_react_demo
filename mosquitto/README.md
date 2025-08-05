# Mosquitto MQTT Broker

## 功能
專案專用的 MQTT Broker，提供訊息中繼服務。

## 啟動方式

### 方式 1: 本機啟動 (推薦)
```bash
cd mosquitto
chmod +x start_local.sh stop_local.sh
./start_local.sh
```

### 方式 2: 手動啟動
```bash
cd mosquitto
mkdir -p data log
mosquitto -c mosquitto.conf -d
```

### 方式 3: 使用 Homebrew 服務
```bash
# 停止現有服務
brew services stop mosquitto

# 啟動自訂配置
mosquitto -c mosquitto.conf -d
```

## 停止服務

### 使用腳本
```bash
./stop_local.sh
```

### 手動停止
```bash
pkill mosquitto
```

## 測試連接

### 1. 檢查服務狀態
```bash
ps aux | grep mosquitto
```

### 2. 查看日誌
```bash
tail -f log/mosquitto.log
```

### 3. 測試 MQTT 連接
```bash
# 訂閱測試
mosquitto_sub -h localhost -t "test" -v

# 發布測試
mosquitto_pub -h localhost -t "test" -m "Hello MQTT"
```

## 配置說明

### 埠號
- **1883**: MQTT 標準埠
- **9001**: WebSocket 埠 (可選)

### 功能
- ✅ 匿名連接 (開發環境)
- ✅ 日誌記錄
- ✅ 數據持久化
- ✅ WebSocket 支援
- ✅ 自動重啟

## 與專案整合

### 修改 sensor.py 連接設定
```python
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
```

### 監控數據流
```bash
# 監聽感測器數據
mosquitto_sub -h localhost -t "env/room01/reading" -v
```

## 故障排除

### 埠號被佔用
```bash
# 檢查埠號使用情況
lsof -i :1883
lsof -i :9001

# 停止佔用進程
sudo lsof -ti:1883 | xargs kill -9
```

### 權限問題
```bash
# 確保目錄權限正確
chmod 755 data log
``` 