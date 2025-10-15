import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,    // X 軸的分類刻度（用於顯示時間標籤）
  LinearScale,      // Y 軸的線性刻度（用於顯示數值）
  PointElement,     // 折線圖上的點
  LineElement,      // 折線
  Title,
  Tooltip,
  Legend,           // 圖例（區分溫度和濕度）
  Filler            // 填充區域（折線下方的漸層色）
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import { API_ENDPOINTS, CONFIG, WS_ENDPOINTS } from './config'
import './App.css'

// 註冊 Chart.js 組件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

interface SensorData {
  timestamp: string
  temperature: number
  humidity: number
}

interface Alert {
  id: number
  message: string
  type: 'warning' | 'danger' | 'info'
  timestamp: string
}

// WebSocket 訊息格式
interface WebSocketMessage {
  type: 'alert'
  data: {
    alert_type: string
    severity: string
    message: string
    timestamp: string
    sensor_data: {
      temp: number
      humidity: number
    }
  }
  broadcast_time: string
}

// 後端 API 回傳的資料格式
interface ApiSensorData {
  id: number
  temp: number
  humidity: number
  timestamp: string
  created_at: string
}

function App() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [historicalData, setHistoricalData] = useState<SensorData[]>([])
  const [isConnected, setIsConnected] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // 格式化時間戳記為圖表顯示格式
  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('zh-TW', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    })
  }

  useEffect(() => {
    const fetchHistoricalData = async () => {
      try {
        setIsLoading(true)
        setError(null)
        
        // 呼叫後端 API 取得最近 N 筆數據
        const response = await fetch(`${API_ENDPOINTS.sensor.readings}?limit=${CONFIG.HISTORY_DATA_LIMIT}`)
        
        if (!response.ok) {
          throw new Error(`HTTP 錯誤！狀態碼: ${response.status}`)
        }
        
        const result = await response.json()
        
        if (result.status === 'success' && result.data) {
          // 後端回傳的資料是降序（最新在前），需要反轉成升序（舊到新）
          const reversedData = [...result.data].reverse()
          
          // 轉換資料格式
          const formattedData: SensorData[] = reversedData.map((item: ApiSensorData) => ({
            timestamp: formatTimestamp(item.timestamp),
            temperature: item.temp,
            humidity: item.humidity
          }))
          
          setHistoricalData(formattedData)
          
          console.log('✅ 成功載入歷史數據，共', formattedData.length, '筆')
        } else {
          throw new Error('API 回傳格式錯誤')
        }
      } catch (err) {
        console.error('❌ 無法取得歷史數據:', err)
        setError(err instanceof Error ? err.message : '未知錯誤')
      } finally {
        setIsLoading(false)
      }
    }

    fetchHistoricalData()
  }, [])

  // WebSocket 連接管理
  useEffect(() => {
    let ws: WebSocket | null = null
    let reconnectTimer: number | null = null
    let isUnmounting = false

    const connectWebSocket = () => {
      try {
        console.log('🔌 正在連接 WebSocket...', WS_ENDPOINTS.alerts)
        ws = new WebSocket(WS_ENDPOINTS.alerts)

        ws.onopen = () => {
          console.log('✅ WebSocket 連線已建立')
          setIsConnected(true)
          setError(null)
        }

        ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data)
            console.log('📨 收到 WebSocket 訊息:', message)

            if (message.type === 'alert') {
              const { severity, message: alertMessage, timestamp } = message.data
              
              // 將嚴重程度映射到警報類型
              const alertType = severity === 'error' ? 'danger' : 
                               severity === 'warning' ? 'warning' : 'info'
              
              // 格式化時間
              const formattedTime = formatTimestamp(timestamp)
              
              // 建立新警報
              const newAlert: Alert = {
                id: Date.now(),
                message: alertMessage,
                type: alertType,
                timestamp: formattedTime
              }

              // 添加警報（限制最大顯示數量）
              setAlerts(prev => {
                const updated = [newAlert, ...prev]
                return updated.slice(0, CONFIG.MAX_ALERTS_DISPLAY)
              })

              console.log('🚨 新增警報:', newAlert)
            }
          } catch (err) {
            console.error('❌ 解析 WebSocket 訊息失敗:', err)
          }
        }

        ws.onerror = (error) => {
          console.error('❌ WebSocket 錯誤:', error)
          setIsConnected(false)
        }

        ws.onclose = () => {
          console.log('🔌 WebSocket 連線已關閉')
          setIsConnected(false)

          // 如果不是主動卸載，則嘗試重新連接
          if (!isUnmounting) {
            console.log('⏰ 5 秒後重新連接...')
            reconnectTimer = setTimeout(() => {
              connectWebSocket()
            }, 5000)
          }
        }
      } catch (err) {
        console.error('❌ WebSocket 連接失敗:', err)
        setError('WebSocket 連接失敗')
        setIsConnected(false)
      }
    }

    // 初始化連接
    connectWebSocket()

    // 清理函數：組件卸載時執行
    return () => {
      isUnmounting = true
      
      if (reconnectTimer) {
        clearTimeout(reconnectTimer)
      }
      
      if (ws) {
        console.log('🧹 清理 WebSocket 連接')
        ws.close()
      }
    }
  }, []) // 空依賴陣列，只在組件掛載時執行一次

  // 準備圖表數據
  const chartData = {
    // labels：X 軸的標籤（時間點）
    labels: historicalData.map(d => d.timestamp),
    // 例如：['14:30', '14:31', '14:32', ...]
    datasets: [
      // 第一條線：溫度
      {
        label: '溫度 (°C)',
        data: historicalData.map(d => d.temperature), // Y 軸數據
        // 例如：[28.5, 29.1, 28.8, ...]
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',  // 填充區域顏色（半透明紅）
        yAxisID: 'y', // 使用左側 Y 軸
        tension: 0.4, // 線條彎曲程度（0=直線，1=很彎）
        fill: true    // 是否填充線條下方區域
      },
      // 第二條線：濕度
      {
        label: '濕度 (%)',
        data: historicalData.map(d => d.humidity),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.1)',
        yAxisID: 'y1', // 使用右側 Y 軸
        tension: 0.4,
        fill: true
      }
    ]
  }

  const chartOptions = {
    responsive: true,   // 是否響應式
    maintainAspectRatio: false,  // 不維持長寬比：讓我們可以用 CSS 控制高度
    // 互動設定
    interaction: {
      mode: 'index' as const,  // 滑鼠移到某個點時，顯示該時間點的所有數據
      intersect: false,    // 不需要精確移到點上，靠近就會顯示
    },
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: '最近30分鐘溫濕度歷史紀錄',
        font: {
          size: 16
        }
      },
    },
    // 座標軸設定
    scales: {
      y: {
        type: 'linear' as const,   // 線性刻度
        display: true,
        position: 'left' as const, // 顯示在左側
        title: {
          display: true,
          text: '溫度 (°C)'
        },
        min: 20,
        max: 35
      },
      // 右側 Y 軸（濕度）
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,   // 顯示在右側
        title: {
          display: true,
          text: '濕度 (%)'
        },
        min: 40,
        max: 90,
        grid: {
          drawOnChartArea: false,   // 不在圖表區域畫網格線（避免和左軸重疊）
        },
      },
    },
  }

  // 關閉警報
  const dismissAlert = (id: number) => {
    setAlerts(prev => prev.filter(alert => alert.id !== id))
  }

  return (
    <div className="app-container">
      {/* 頂部標題列 */}
      <header className="app-header">
        <h1>🏠 室內環境監控系統</h1>
        <div className="connection-status">
          <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
          <span>{isConnected ? 'WebSocket 已連線' : 'WebSocket 連線中...'}</span>
        </div>
      </header>

      {/* 錯誤提示 */}
      {error && (
        <div className="alert alert-danger">
          <div className="alert-content">
            <span className="alert-message">⚠️ 連線錯誤：{error}</span>
            <span className="alert-time">使用假資料顯示</span>
          </div>
        </div>
      )}

      {/* 載入中提示 */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner">載入中...</div>
        </div>
      )}

      {/* 警報通知區 */}
      {alerts.length > 0 && (
        <div className="alert-section">
          {alerts.map(alert => (
            <div key={alert.id} className={`alert alert-${alert.type}`}>
              <div className="alert-content">
                <span className="alert-message">{alert.message}</span>
                <span className="alert-time">{alert.timestamp}</span>
              </div>
              <button className="alert-close" onClick={() => dismissAlert(alert.id)}>
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      {/* 主要內容區 */}
      <div className="main-content">
        {/* 圖表區域 */}
        <div className="chart-section">
          <div className="chart-container">
            <Line data={chartData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
