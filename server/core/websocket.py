#!/usr/bin/env python3
"""
WebSocket 連線管理
處理 WebSocket 連線的建立、關閉和訊息推播
"""

from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

class ConnectionManager:
    """管理 WebSocket 連線"""
    
    def __init__(self):
        """初始化連線管理器"""
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        """處理新的 WebSocket 連線"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 WebSocket 連線建立 - 目前連線數: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        """處理 WebSocket 連線關閉"""
        self.active_connections.remove(websocket)
        print(f"🔌 WebSocket 連線關閉 - 目前連線數: {len(self.active_connections)}")
        
    async def broadcast_alert(self, alert_data: dict):
        """向所有連線的客戶端推播警報"""
        # 準備推播資料
        message = {
            "type": "alert",
            "data": alert_data,
            "broadcast_time": datetime.utcnow().isoformat() + "Z"
        }
        
        # 推播給所有連線中的客戶端
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected_clients.append(connection)
            except Exception as e:
                print(f"❌ 推播警報時發生錯誤: {e}")
                disconnected_clients.append(connection)
                
        # 移除已斷線的客戶端
        for client in disconnected_clients:
            self.disconnect(client)
            
        print(f"📢 警報已推播給 {len(self.active_connections)} 個連線")

# 建立全域的連線管理器實例
manager = ConnectionManager()
