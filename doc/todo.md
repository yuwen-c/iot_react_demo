# 前端

## tech stack

技術選型確認
框架：Vite + React + TypeScript
UI 組件庫：Material UI (MUI)
WebSocket 即時通訊
圖表視覺化
狀態管理：React 內建（useState/useContext）

## 必要的 npm 套件規劃

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

## 細節

### 即時數據處理架構

需要處理兩種數據流：
WebSocket 即時警報：當 controller 偵測到異常時推播
輪詢或初始載入：定期取得感測器歷史數據
需考慮 WebSocket 重連機制、錯誤處理

### UI/UX 功能規劃

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

## 歷史數據，和即時數據，不放在同一個 chart
