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
import { API_ENDPOINTS, CONFIG } from './config'
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
  type: 'warning' | 'danger'
  timestamp: string
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
  const [currentTemp, setCurrentTemp] = useState<number>(0)
  const [currentHumidity, setCurrentHumidity] = useState<number>(0)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [historicalData, setHistoricalData] = useState<SensorData[]>([])
  const [isConnected] = useState<boolean>(true) // 之後會連接真實 WebSocket
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
          
          // 設定當前數值為最新一筆（陣列最後一個）
          if (formattedData.length > 0) {
            const latest = formattedData[formattedData.length - 1]
            setCurrentTemp(latest.temperature)
            setCurrentHumidity(latest.humidity)
          }
          
          console.log('✅ 成功載入歷史數據，共', formattedData.length, '筆')
        } else {
          throw new Error('API 回傳格式錯誤')
        }
      } catch (err) {
        console.error('❌ 無法取得歷史數據:', err)
        setError(err instanceof Error ? err.message : '未知錯誤')
        
        // 發生錯誤時使用假資料（fallback）
        console.log('⚠️ 使用假資料作為備援')
        // generateFallbackData()
      } finally {
        setIsLoading(false)
      }
    }

    // 備援：生成假資料（當 API 連線失敗時使用）
    // const generateFallbackData = () => {
    //   const data: SensorData[] = []
    //   const now = new Date()
      
    //   for (let i = 29; i >= 0; i--) {
    //     const time = new Date(now.getTime() - i * 60000) // 每分鐘一筆
    //     data.push({
    //       timestamp: time.toLocaleTimeString('zh-TW', { 
    //         hour: '2-digit', 
    //         minute: '2-digit',
    //         second: '2-digit'
    //       }),
    //       temperature: 25 + Math.random() * 8,
    //       humidity: 50 + Math.random() * 30
    //     })
    //   }
      
    //   setHistoricalData(data)
    //   if (data.length > 0) {
    //     const latest = data[data.length - 1]
    //     setCurrentTemp(latest.temperature)
    //     setCurrentHumidity(latest.humidity)
    //   }
    // }

    fetchHistoricalData()
  }, [])

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
        text: '溫濕度歷史趨勢（最近 30 分鐘）',
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
          <span>{isConnected ? 'API 已連線' : '連線中斷'}</span>
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
        {/* 即時狀態卡區 */}
        <div className="status-cards">
          <div className="status-card temperature-card">
            <div className="card-icon">🌡️</div>
            <div className="card-content">
              <h3 className="card-label">溫度</h3>
              <div className="card-value">{currentTemp.toFixed(1)}<span className="unit">°C</span></div>
              <div className="card-status">
                {currentTemp > 30 ? '⚠️ 偏高' : currentTemp < 20 ? '❄️ 偏低' : '✅ 正常'}
              </div>
            </div>
          </div>

          <div className="status-card humidity-card">
            <div className="card-icon">💧</div>
            <div className="card-content">
              <h3 className="card-label">濕度</h3>
              <div className="card-value">{currentHumidity.toFixed(1)}<span className="unit">%</span></div>
              <div className="card-status">
                {currentHumidity > 70 ? '💦 偏高' : currentHumidity < 40 ? '🏜️ 偏低' : '✅ 正常'}
              </div>
            </div>
          </div>
        </div>

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
