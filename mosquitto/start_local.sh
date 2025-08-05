#!/bin/bash

echo "🚀 啟動本機 Mosquitto MQTT Broker..."

# 檢查 Mosquitto 是否安裝（支援 Homebrew 安裝路徑）
MOSQUITTO_PATH=""
if command -v mosquitto &> /dev/null; then
    MOSQUITTO_PATH=$(which mosquitto)
elif [ -f "/opt/homebrew/sbin/mosquitto" ]; then
    MOSQUITTO_PATH="/opt/homebrew/sbin/mosquitto"
elif [ -f "/usr/local/sbin/mosquitto" ]; then
    MOSQUITTO_PATH="/usr/local/sbin/mosquitto"
else
    echo "❌ Mosquitto 未安裝，請先執行："
    echo "   brew install mosquitto"
    exit 1
fi

echo "📡 使用 Mosquitto 路徑: $MOSQUITTO_PATH"

# 建立必要的目錄
mkdir -p data log

# 停止現有的 Mosquitto 服務
echo "🛑 停止現有的 Mosquitto 服務..."
brew services stop mosquitto 2>/dev/null || true
pkill mosquitto 2>/dev/null || true

# 啟動 Mosquitto 使用自訂配置
echo "📡 啟動 Mosquitto 使用自訂配置..."
"$MOSQUITTO_PATH" -c mosquitto.conf -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 3

# 檢查服務是否啟動
if pgrep -x "mosquitto" > /dev/null; then
    echo "✅ Mosquitto 啟動成功！"
    echo "📡 服務位址: localhost:1883"
    echo "🌐 WebSocket: localhost:9001"
    echo ""
    echo "📋 測試指令:"
    echo "  mosquitto_sub -h localhost -t 'test' -v"
    echo "  mosquitto_pub -h localhost -t 'test' -m 'Hello'"
    echo ""
    echo "📊 查看日誌:"
    echo "  tail -f log/mosquitto.log"
    echo ""
    echo "🛑 停止服務:"
    echo "  pkill mosquitto"
else
    echo "❌ Mosquitto 啟動失敗"
    echo "📊 查看錯誤日誌:"
    echo "  tail -f log/mosquitto.log"
    exit 1
fi 