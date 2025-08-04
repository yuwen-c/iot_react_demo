#!/usr/bin/env python3
"""
MQTT 連接測試腳本
用於測試 Mosquitto Broker 是否正常運作
"""

import paho.mqtt.client as mqtt
import time
import json

def on_connect(client, userdata, flags, rc):
    """連接成功回調"""
    if rc == 0:
        print("✅ MQTT Broker 連接成功！")
        # 訂閱測試 topic
        client.subscribe("test/topic")
    else:
        print(f"❌ 連接失敗，錯誤碼: {rc}")

def on_message(client, userdata, msg):
    """接收訊息回調"""
    print(f"📨 收到訊息: {msg.topic} -> {msg.payload.decode()}")

def on_publish(client, userdata, mid):
    """發布成功回調"""
    print(f"📤 測試訊息已發布 (ID: {mid})")

def test_mqtt_connection():
    """測試 MQTT 連接"""
    print("🧪 開始測試 MQTT 連接...")
    
    # 建立客戶端
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    
    try:
        # 連接到本地 Mosquitto
        client.connect("localhost", 1883, 60)
        client.loop_start()
        
        # 等待連接
        time.sleep(2)
        
        # 發布測試訊息
        test_message = {
            "test": True,
            "message": "MQTT 連接測試",
            "timestamp": time.time()
        }
        
        client.publish("test/topic", json.dumps(test_message))
        
        # 等待接收訊息
        time.sleep(3)
        
        print("✅ MQTT 測試完成！")
        
    except Exception as e:
        print(f"❌ MQTT 測試失敗: {e}")
        print("💡 請確認 Mosquitto 是否已啟動:")
        print("   brew services start mosquitto")
        
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    test_mqtt_connection() 