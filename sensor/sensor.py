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
        
        # 週期性異常模式的計數器
        self.publish_count = 0
        self.abnormal_interval = 5  # 每隔 5 次發送一次異常數據
        
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
        """生成模擬感測器數據（正常範圍內）"""
        # 模擬真實環境的溫濕度變化
        base_temp = 25.0
        base_humidity = 52.0
        
        # 添加隨機變化（確保不觸發警報）
        temp = base_temp + random.uniform(-3, 4)  # 22-29°C（不超過閾值 30°C）
        humidity = base_humidity + random.uniform(-10, 13)  # 42-65%（不低於閾值 40%）
        
        # 確保在安全範圍內
        temp = max(20, min(29, temp))
        humidity = max(42, min(65, humidity))
        
        return {
            "temp": round(temp, 1),
            "humidity": round(humidity, 1),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def generate_abnormal_sensor_data(self):
        """生成異常感測器數據（用於觸發警報測試）"""
        # 隨機選擇異常類型：高溫或低濕度
        anomaly_type = random.choice(['high_temp', 'low_humidity', 'both'])
        
        if anomaly_type == 'high_temp':
            # 生成高溫異常數據（超過閾值 30°C）
            temp = Config.TEMP_THRESHOLD + random.uniform(1, 8)  # 31-38°C
            humidity = random.uniform(45, 65)  # 正常濕度
            
        elif anomaly_type == 'low_humidity':
            # 生成低濕度異常數據（低於閾值 40%）
            temp = random.uniform(22, 28)  # 正常溫度
            humidity = Config.HUMIDITY_THRESHOLD - random.uniform(5, 15)  # 25-35%
            
        else:  # both - 同時異常
            # 同時觸發高溫和低濕度警報
            temp = Config.TEMP_THRESHOLD + random.uniform(1, 8)  # 31-38°C
            humidity = Config.HUMIDITY_THRESHOLD - random.uniform(5, 15)  # 25-35%
        
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
        print(f"🚨 異常數據週期: 每 {self.abnormal_interval} 次發送一次異常數據")
        print("-" * 50)
        
        if not self.connect():
            return
            
        try:
            while True:
                self.publish_count += 1
                
                # 週期性發送異常數據
                if self.publish_count % self.abnormal_interval == 0:
                    # 生成異常感測器數據
                    data = self.generate_abnormal_sensor_data()
                    is_abnormal = True
                else:
                    # 生成正常感測器數據
                    data = self.generate_sensor_data()
                    is_abnormal = False
                
                # 發布數據
                self.publish_data(data)
                
                # 顯示數據（異常數據用特殊標記）
                status_icon = "🚨" if is_abnormal else "📊"
                status_text = " [異常數據]" if is_abnormal else ""
                print(f"{status_icon} #{self.publish_count} 溫度: {data['temp']}°C, 濕度: {data['humidity']}%{status_text}")
                
                # 等待5秒
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 感測器已停止")
            print(f"📊 總共發送: {self.publish_count} 筆數據")
            self.client.loop_stop()
            self.client.disconnect()

if __name__ == "__main__":
    sensor = SensorSimulator()
    sensor.run() 