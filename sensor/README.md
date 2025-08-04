# Sensor 模組

## 功能
模擬環境感測器，定期發送溫濕度數據到 MQTT Broker。

## 檔案說明
- `sensor.py` - 主要感測器模擬程式
- `test_mqtt.py` - MQTT 連接測試腳本

## 使用方法

### 1. 測試 MQTT 連接
```bash
# 確保 Mosquitto 已啟動
brew services start mosquitto

# 測試 MQTT 連接
python test_mqtt.py
```

### 2. 啟動感測器
```bash
# 啟動感測器模擬器
python sensor.py
```

### 3. 監聽數據
在另一個終端中監聽感測器數據：
```bash
mosquitto_sub -h localhost -t "env/room01/reading" -v
```

## 環境變數
可以透過環境變數自訂配置：
```bash
export MQTT_BROKER=localhost
export MQTT_PORT=1883
export MQTT_TOPIC=env/room01/reading
```

## 數據格式
感測器發送的 JSON 數據格式：
```json
{
  "temp": 26.5,
  "humidity": 45.2,
  "timestamp": "2025-01-27T10:30:00Z"
}
```

## 特性
- 每 5 秒發送一次數據
- 溫度範圍：22-30°C
- 濕度範圍：20-80%
- 支援 QoS 1 確保數據傳遞
- 自動重連機制 