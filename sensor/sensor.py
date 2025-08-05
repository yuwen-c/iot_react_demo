#!/usr/bin/env python3
"""
模擬環境感測器
每5秒發送溫濕度數據到MQTT Broker
"""

import json
import os
import sys
import time
import random
from datetime import datetime
import paho.mqtt.client as mqtt

# 添加專案根目錄到 Python 路徑，以便導入 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class SensorSimulator:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
    def on_connect(self, client, userdata, flags, rc):
        """連接成功回調"""
        if rc == 0:
            print(f"✅ 已連接到 MQTT Broker: {Config.MQTT_BROKER}:{Config.MQTT_PORT}")
        else:
            print(f"❌ 連接失敗，錯誤碼: {rc}")
            
    def on_publish(self, client, userdata, mid):
        """發布成功回調"""
        print(f"📤 數據已發布 (ID: {mid})")
        
    def generate_sensor_data(self):
        """生成模擬感測器數據"""
        # 模擬真實環境的溫濕度變化
        base_temp = 25.0
        base_humidity = 50.0
        
        # 添加隨機變化
        temp = base_temp + random.uniform(-3, 5)  # 22-30°C
        humidity = base_humidity + random.uniform(-15, 15)  # 35-65%
        
        # 確保濕度在合理範圍內
        humidity = max(20, min(80, humidity))
        
        return {
            "temp": round(temp, 1),
            "humidity": round(humidity, 1),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    def connect(self):
        """連接到 MQTT Broker"""
        try:
            self.client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"❌ 連接 MQTT Broker 失敗: {e}")
            return False
            
    def publish_data(self, data):
        """發布數據到 MQTT Topic"""
        message = json.dumps(data, ensure_ascii=False)
        result = self.client.publish(Config.MQTT_TOPIC, message, qos=1)
        return result
        
    def run(self):
        """主運行循環"""
        print("🚀 啟動環境感測器模擬器...")
        print(f"📡 目標 MQTT Broker: {Config.MQTT_BROKER}:{Config.MQTT_PORT}")
        print(f"📋 發布 Topic: {Config.MQTT_TOPIC}")
        print("⏰ 數據發送間隔: 5秒")
        print("-" * 50)
        
        if not self.connect():
            return
            
        try:
            while True:
                # 生成感測器數據
                data = self.generate_sensor_data()
                
                # 發布數據
                self.publish_data(data)
                
                # 顯示數據
                print(f"📊 溫度: {data['temp']}°C, 濕度: {data['humidity']}%")
                
                # 等待5秒
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 感測器已停止")
            self.client.loop_stop()
            self.client.disconnect()

if __name__ == "__main__":
    sensor = SensorSimulator()
    sensor.run() 