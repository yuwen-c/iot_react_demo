#!/usr/bin/env python3
"""
環境監控控制器
訂閱 MQTT 感測器數據，判斷警報條件，處理異常情況，寫入資料庫
"""

import json
import os
import sys
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import httpx

# 添加專案根目錄到 Python 路徑，以便導入 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from database import DatabaseManager

class EnvironmentController:
    def __init__(self):
        """初始化環境控制器"""
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # 初始化資料庫管理器
        self.db = DatabaseManager()
        
        # 初始化 HTTP 客戶端（用於通知 Web Server）
        self.http_client = httpx.Client(timeout=5.0)
        
        # 統計數據
        self.message_count = 0
        self.alert_count = 0
        
    def on_connect(self, client, userdata, flags, rc):
        """MQTT 連接成功回調"""
        if rc == 0:
            print(f"✅ 控制器已連接到 MQTT Broker: {Config.MQTT_BROKER}:{Config.MQTT_PORT}")
            # 訂閱感測器數據 topic
            client.subscribe(Config.MQTT_TOPIC, qos=1)
            print(f"📡 已訂閱 Topic: {Config.MQTT_TOPIC}")
        else:
            print(f"❌ 連接失敗，錯誤碼: {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        """MQTT 斷線回調"""
        if rc != 0:
            print(f"⚠️ 意外斷線，錯誤碼: {rc}")
        else:
            print("🔌 正常斷線")
            
    def on_message(self, client, userdata, msg):
        """接收 MQTT 訊息回調"""
        try:
            # 解析 JSON 數據
            data = json.loads(msg.payload.decode('utf-8'))
            self.message_count += 1
            
            # 提取數據
            temp = data.get('temp', 0)
            humidity = data.get('humidity', 0)
            timestamp = data.get('timestamp', '')
            
            print(f"📊 收到數據 #{self.message_count}")
            print(f"   溫度: {temp}°C, 濕度: {humidity}%")
            print(f"   時間: {timestamp}")
            
            # 儲存感測器數據到資料庫
            if self.db.save_sensor_reading(data):
                print("   儲存: ✅ 已寫入資料庫")
            else:
                print("   儲存: ❌ 寫入資料庫失敗")
            
            # 檢查警報條件
            alerts = self.check_alerts(temp, humidity)
            
            # 處理警報
            if alerts:
                self.handle_alerts(alerts, data)
            else:
                print("   狀態: ✅ 正常")
                
            print("-" * 50)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析錯誤: {e}")
        except Exception as e:
            print(f"❌ 處理訊息時發生錯誤: {e}")
            
    def check_alerts(self, temp, humidity):
        """檢查警報條件"""
        alerts = []
        
        # 檢查溫度警報
        if temp > Config.TEMP_THRESHOLD:
            alerts.append({
                'type': 'high_temperature',
                'message': f'高溫警報！當前溫度 {temp}°C 超過閾值 {Config.TEMP_THRESHOLD}°C',
                'severity': 'warning'
            })
            
        # 檢查濕度警報
        if humidity < Config.HUMIDITY_THRESHOLD:
            alerts.append({
                'type': 'low_humidity',
                'message': f'低濕度警報！當前濕度 {humidity}% 低於閾值 {Config.HUMIDITY_THRESHOLD}%',
                'severity': 'warning'
            })
            
        return alerts
        
    def handle_alerts(self, alerts, data):
        """處理警報"""
        self.alert_count += len(alerts)
        
        for alert in alerts:
            print(f"🚨 警報 #{self.alert_count}: {alert['message']}")
            
            # 準備警報資料
            alert_data = {
                'alert_type': alert['type'],
                'severity': alert['severity'],
                'message': alert['message'],
                'timestamp': datetime.utcnow().isoformat() + "Z",
                'sensor_data': data
            }
            
            # 儲存警報到資料庫
            if self.db.save_alert(alert_data):
                print(f"   儲存: ✅ 警報已寫入資料庫")
            else:
                print(f"   儲存: ❌ 警報寫入資料庫失敗")
            
            # 發送 HTTP 通知到 Web Server
            self.send_alert_to_server(alert_data)
    
    def send_alert_to_server(self, alert_data):
        """發送警報通知到 Web Server"""
        try:
            # 構建 API URL
            api_url = f"{Config.WEB_SERVER_URL}/api/alerts/notify"
            
            # 發送 POST 請求
            response = self.http_client.post(api_url, json=alert_data)
            
            if response.status_code == 200:
                print(f"   通知: ✅ 已發送到 Web Server")
                print(f"   回應: {response.json().get('message', 'OK')}")
            else:
                print(f"   通知: ⚠️ Web Server 回應異常 (狀態碼: {response.status_code})")
                print(f"   錯誤: {response.text}")
                
        except httpx.ConnectError:
            print(f"   通知: ❌ 無法連接到 Web Server ({Config.WEB_SERVER_URL})")
        except httpx.TimeoutException:
            print(f"   通知: ⏱️ 連接 Web Server 超時")
        except Exception as e:
            print(f"   通知: ❌ 發送失敗: {e}")
        
    def connect(self):
        """連接到 MQTT Broker"""
        try:
            print(f"🔗 正在連接到 MQTT Broker: {Config.MQTT_BROKER}:{Config.MQTT_PORT}")
            self.client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"❌ 連接 MQTT Broker 失敗: {e}")
            return False
            
    def disconnect(self):
        """斷開 MQTT 連接並關閉 HTTP 客戶端"""
        self.client.loop_stop()
        self.client.disconnect()
        self.http_client.close()
        
    def get_stats(self):
        """取得統計資訊"""
        db_stats = self.db.get_statistics()
        return {
            'message_count': self.message_count,
            'alert_count': self.alert_count,
            'connected': self.client.is_connected(),
            'db_total_readings': db_stats['total_readings'],
            'db_total_alerts': db_stats['total_alerts'],
            'db_today_readings': db_stats['today_readings'],
            'db_today_alerts': db_stats['today_alerts']
        }
        
    def run(self):
        """主運行循環"""
        print("🚀 啟動環境監控控制器...")
        print(f"📡 目標 MQTT Broker: {Config.MQTT_BROKER}:{Config.MQTT_PORT}")
        print(f"📋 訂閱 Topic: {Config.MQTT_TOPIC}")
        print(f"🌐 Web Server URL: {Config.WEB_SERVER_URL}")
        print(f"🚨 溫度閾值: {Config.TEMP_THRESHOLD}°C")
        print(f"🚨 濕度閾值: {Config.HUMIDITY_THRESHOLD}%")
        print(f"💾 資料庫路徑: {self.db.db_path}")
        print("-" * 50)
        
        if not self.connect():
            return
            
        try:
            while True:
                # 每 30 秒顯示一次統計資訊
                time.sleep(30)
                stats = self.get_stats()
                print(f"📈 統計: 收到 {stats['message_count']} 筆數據, 觸發 {stats['alert_count']} 次警報")
                print(f"💾 資料庫: 總計 {stats['db_total_readings']} 筆讀數, {stats['db_total_alerts']} 筆警報")
                
        except KeyboardInterrupt:
            print("\n🛑 控制器已停止")
            stats = self.get_stats()
            print(f"📊 最終統計: 收到 {stats['message_count']} 筆數據, 觸發 {stats['alert_count']} 次警報")
            print(f"💾 資料庫統計: {stats['db_total_readings']} 筆讀數, {stats['db_total_alerts']} 筆警報")
            self.disconnect()

if __name__ == "__main__":
    controller = EnvironmentController()
    controller.run() 