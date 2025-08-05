# 室內環境監控與警報系統

## 1. 專案背景

本系統模擬一個室內環境監控場景（如資料中心、實驗室等），用於即時監測室內溫度與濕度，並在環境異常時發出警報提醒使用者，提升環境安全與設備運作穩定性。

## 2. 功能需求

2.1 感測資料模擬
使用 sensor.py 模擬溫度與濕度感測器數據

模擬資料每 5 秒鐘發送一次

資料格式 JSON，例如：

```json
{
  "temp": 29.5,
  "humidity": 38.2,
  "timestamp": "2025-08-04T12:00:00Z"
}
```

2.2 MQTT 通訊
使用 Eclipse Mosquitto 作為 MQTT Broker

sensor.py 將資料發布至指定 Topic（例如 env/room01/reading）

controller.py 作為 MQTT client 訂閱此 Topic

2.3 資料判斷與警報
使用 Python 撰寫 controller.py，作為 MQTT Client 訂閱感測器資料

若溫度 > 30°C

或濕度 < 40%

則透過 HTTP 通知 Web Server 發送警報訊息

警報訊息包含警告類型、當前溫濕度與提示文字

2.4 數據持久化與歷史記錄
使用 SQLite 資料庫進行數據持久化

建立共享資料庫檔案 `data/environment.db`

controller.py 將所有感測數據儲存至共享 SQLite 資料庫

建立兩個主要資料表：
- sensor_readings：儲存所有感測數據
- alert_history：記錄所有警報事件

Web Server 提供數據查詢 API，支援歷史數據檢視與統計分析

2.5 Web Server 與前端顯示
使用 FastAPI 提供 REST API 與 WebSocket 服務

接收來自 controller.py 的 HTTP 警報通知

透過 WebSocket 即時推播警報給前端

前端使用 React 框架，搭配圖表套件（Chart.js 或 Recharts）

顯示溫度與濕度的即時折線圖

接收並呈現警報通知（視覺彈跳或聲音提示）

提供歷史數據查詢與警報歷史記錄檢視功能

## 3. 技術架構概述

```mermaid
sensor.py → MQTT Broker (Mosquitto) ←→ controller.py → SQLite DB (data/environment.db)
                      ↑                           ↓                    ↑
                 資料發布與訂閱              HTTP 警報通知        Web Server (FastAPI)
                                                                    ↓
                                                              WebSocket ←→ React 前端
```

sensor.py：模擬感測器，負責資料產生與發布

Mosquitto：負責 MQTT 通訊中繼

controller.py：訂閱 MQTT，判斷警報，數據持久化，HTTP 通知 Web Server

SQLite DB (data/environment.db)：共享資料庫，儲存感測數據與警報歷史

FastAPI Web Server：提供前端頁面、REST API、接收 HTTP 警報通知及 WebSocket 即時推播

React 前端：顯示資料視覺化、警報提示與歷史數據查詢

## 4. 開發與部署環境

使用 Python 技術棧：

MQTT Client：paho-mqtt

Web Server：FastAPI + uvicorn

HTTP 通訊：requests (controller 通知 Web Server)

WebSocket：FastAPI 內建 WebSocket 支援

資料庫：SQLite（Python 內建支援）

使用 Docker 容器化部署，並用 docker-compose 管理各服務

React 使用 Vite 作為開發與建置工具

## 5. 預期效益

實現 IoT 常見資料流向與即時通訊

練習 MQTT Broker 與 MQTT Client 與感測器模擬

練習 HTTP 服務間通訊與 WebSocket 即時推播機制

強化 React 前端即時資料視覺化能力

學習數據持久化與歷史記錄管理

模擬實際環境監控情境，具備良好擴充性與通用性
