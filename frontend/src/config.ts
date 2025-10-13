/**
 * API 配置文件
 * 集中管理所有 API 端點
 */

// API 基礎 URL
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// WebSocket URL
export const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

// API 端點
export const API_ENDPOINTS = {
  // 感測器相關
  sensor: {
    latest: `${API_BASE_URL}/api/sensor/latest`,
    readings: `${API_BASE_URL}/api/sensor/readings`,
    readingsRange: `${API_BASE_URL}/api/sensor/readings/range`,
    statistics: `${API_BASE_URL}/api/sensor/statistics`,
  },
  
  // 警報相關
  alerts: {
    history: `${API_BASE_URL}/api/alerts/history`,
    historyRange: `${API_BASE_URL}/api/alerts/history/range`,
    statistics: `${API_BASE_URL}/api/alerts/statistics`,
  },
  
  // 系統相關
  health: `${API_BASE_URL}/api/health`,
  config: `${API_BASE_URL}/api/config`,
}

// WebSocket 端點
export const WS_ENDPOINTS = {
  alerts: `${WS_BASE_URL}/ws/alerts`,
  sensor: `${WS_BASE_URL}/ws/sensor`, // 未來可能會用到
}

// 預設配置
export const CONFIG = {
  // 歷史數據筆數
  HISTORY_DATA_LIMIT: 30,
  
  // 圖表刷新間隔（毫秒）
  CHART_UPDATE_INTERVAL: 5000,
  
  // 最大顯示警報數
  MAX_ALERTS_DISPLAY: 3,
  
  // 請求超時時間（毫秒）
  REQUEST_TIMEOUT: 10000,
}

