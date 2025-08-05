#!/bin/bash

echo "🛑 停止本機 Mosquitto MQTT Broker..."

# 停止 Mosquitto 進程
if pgrep -x "mosquitto" > /dev/null; then
    echo "📡 停止 Mosquitto 進程..."
    pkill mosquitto
    sleep 2
    
    if pgrep -x "mosquitto" > /dev/null; then
        echo "⚠️  強制停止 Mosquitto..."
        pkill -9 mosquitto
    fi
    
    echo "✅ Mosquitto 已停止"
else
    echo "ℹ️  Mosquitto 未在運行"
fi

# 停止 Homebrew 服務
echo "🛑 停止 Homebrew Mosquitto 服務..."
brew services stop mosquitto 2>/dev/null || true

echo "✅ 所有 Mosquitto 服務已停止" 