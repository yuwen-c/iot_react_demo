-- 環境監控系統資料庫 Schema
-- 建立時間: 2025-01-27

-- 感測器讀數表
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp REAL NOT NULL,
    humidity REAL NOT NULL,
    timestamp TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 警報歷史表
CREATE TABLE IF NOT EXISTS alert_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    sensor_data TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    sent_to_frontend BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 建立索引以提高查詢效能
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp 
ON sensor_readings(timestamp);

CREATE INDEX IF NOT EXISTS idx_alert_history_timestamp 
ON alert_history(timestamp);

CREATE INDEX IF NOT EXISTS idx_alert_history_sent 
ON alert_history(sent_to_frontend);

-- 建立索引以提高統計查詢效能
CREATE INDEX IF NOT EXISTS idx_sensor_readings_created_at 
ON sensor_readings(created_at);

CREATE INDEX IF NOT EXISTS idx_alert_history_created_at 
ON alert_history(created_at); 