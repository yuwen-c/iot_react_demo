# 前端 todo


## 需求

我想用：
1. vite + react 專案，
2. 使用 typescript，
3. 先不需要複雜的 UI 設定，只要一個頁面就好，
4. 先不用考慮跟後端端點整合，
5. 也先不需要考慮 websocket 功能，之後再加
6. 也先不需要考慮數據視覺化功能，之後再加
7. 狀態管理預計會很簡單，不會有複雜的狀態
8. UI 組建，請用 material UI

## tech stack

技術選型確認
框架：Vite + React + TypeScript
UI 組件庫：Material UI (MUI)
頁面結構：單一頁面應用
暫不實作：
後端 API 整合
WebSocket 即時通訊
圖表視覺化
狀態管理：React 內建（useState/useContext）

## todo

1. 專案初始化工具選擇
1. 與後端整合的關鍵點
根據你的 server/main.py，後端已經準備好：
CORS 設定：已允許 localhost:5173 (Vite) 和 localhost:3000 (CRA)
WebSocket 端點：ws://localhost:8000/ws/alerts - 用於即時警報推播
REST API 端點：
/api/health - 健康檢查
/api/config - 系統配置
/api/alerts/history - 警報歷史
/api/alerts/statistics - 警報統計
/api/sensor/* - 感測器數據查詢

1. 必要的 npm 套件規劃
核心框架：react, react-dom
路由：react-router-dom (如果有多頁面需求)
HTTP 請求：axios 或 fetch (內建)
WebSocket：原生 WebSocket API 或 socket.io-client
數據視覺化：chart.js + react-chartjs-2 (README 已提到)
狀態管理：
簡單場景：React Context + useState/useReducer
複雜場景：zustand 或 redux-toolkit
UI 組件庫（可選）：
antd / Material-UI / shadcn/ui
或使用 Tailwind CSS 自建
1. 即時數據處理架構
需要處理兩種數據流：
WebSocket 即時警報：當 controller 偵測到異常時推播
輪詢或初始載入：定期取得感測器歷史數據
需考慮 WebSocket 重連機制、錯誤處理

1. UI/UX 功能規劃
基於你的系統，前端應包含：
即時監控儀表板：顯示當前溫濕度
歷史數據圖表：使用 Chart.js 繪製趨勢
警報通知：即時顯示警報（WebSocket 推送）
警報歷史查詢：篩選、分頁
統計資訊：警報統計、系統狀態

frontend/
├── src/
│   ├── components/        # UI 組件
│   ├── App.tsx           # 主應用
│   ├── main.tsx          # 入口
│   └── theme.ts          # MUI 主題配置
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env

🎨 初始頁面規劃
會建立一個簡單的環境監控儀表板框架，包含：
基本的 Material UI 佈局（AppBar, Container）
預留溫濕度顯示區域（使用 Card）
預留警報通知區域
使用 Material UI 的現代化設計

確認後我會執行以下步驟：
ok在 frontend/ 目錄初始化 Vite + React + TypeScript 專案
ok安裝 Material UI 及相關依賴
ok設定 TypeScript 配置
建立基本的專案結構
建立簡單的儀表板 UI 框架（純前端，先用假資料）
設定 MUI 主題

