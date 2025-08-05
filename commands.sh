uv init --python 3.11
For more details, please visit https://support.apple.com/kb/HT208050.
MacBook-Air-de-marina:iot-react-demo marina$ uv init --python 3.11
Initialized project `iot-react-demo`
MacBook-Air-de-marina:iot-react-demo marina$


更新 pyproject.toml 來包含所有模組需要的依賴

uv sync
Using CPython 3.11.4 interpreter at: /usr/local/bin/python3.11
Creating virtual environment at: .venv
  × No solution found when resolving dependencies:
  ╰─▶ Because sqlite3 was not found in the package registry and your project depends on
      sqlite3, we can conclude that your project's requirements are unsatisfiable.
      And because your project requires iot-react-demo[dev], we can conclude that your
      project's requirements are unsatisfiable.
MacBook-Air-de-marina:iot-react-demo marina$

-> 移除 sqlite3 依賴

uv sync
MacBook-Air-de-marina:iot-react-demo marina$ uv sync
Resolved 36 packages in 967ms
Prepared 34 packages in 849ms
Installed 34 packages in 23ms
 + annotated-types==0.7.0
 + anyio==4.9.0
 + black==25.1.0
 + click==8.2.1
 + fastapi==0.116.1
 + flake8==7.3.0
 + h11==0.16.0
 + httptools==0.6.4
 + idna==3.10
 + iniconfig==2.1.0
 + mccabe==0.7.0
 + mypy-extensions==1.1.0
 + packaging==25.0
 + paho-mqtt==2.1.0
 + pathspec==0.12.1
 + platformdirs==4.3.8
 + pluggy==1.6.0
 + pycodestyle==2.14.0
 + pydantic==2.11.7
 + pydantic-core==2.33.2
 + pyflakes==3.4.0
 + pygments==2.19.2
 + pytest==8.4.1
 + python-dotenv==1.1.1
 + python-multipart==0.0.20
 + pyyaml==6.0.2
 + sniffio==1.3.1
 + starlette==0.47.2
 + typing-extensions==4.14.1
 + typing-inspection==0.4.1
 + uvicorn==0.35.0
 + uvloop==0.21.0
 + watchfiles==1.1.0
 + websockets==15.0.1

 
# 啟動虛擬環境
source .venv/bin/activate

# 安裝 Mosquitto (才有辦法開發 sensor.py)
brew install mosquitto


# ==== 兩種啟動mosquitto的方式 ====
#方法一：直接用brew service，會使用預設的檔案位置

## 啟動 Mosquitto
brew services start mosquitto
==> Successfully started `mosquitto` (label: homebrew.mxcl.mosquitto)

## 關閉 Mosquitto
brew services stop mosquitto
Stopping `mosquitto`... (might take a while)
==> Successfully stopped `mosquitto` (label: homebrew.mxcl.mosquitto)

# 方法二：寫好 mosquitto/mosquitto.conf，並且指定用這個檔案啟動。已經寫好啟動的script:
## 開始
mosquitto/start_local.sh
## 停止
mosquitto/stop_local.sh

# ====== sensor.py 開發======
# 啟動 sensor.py
uv run sensor/sensor.py

# 訂閱 topic，在另一個 terminal 中監聽數據
mosquitto_sub -h localhost -t "env/room01/reading" -v

env/room01/reading {"temp": 25.3, "humidity": 51.3, "timestamp": "2025-08-04T09:18:22.047773Z"}
env/room01/reading {"temp": 22.2, "humidity": 45.5, "timestamp": "2025-08-04T09:18:27.053150Z"}
env/room01/reading {"temp": 29.0, "humidity": 50.4, "timestamp": "2025-08-04T09:18:32.058365Z"}

# 測試
uv run sensor/test_mqtt.py

#===== database 初始化設定 =====

# 初始化資料庫
uv run data/init_db.py
# 資料庫會建立在：根目錄的 data/environment.db

# 測試資料庫 controller 是否可正常連上db
uv run controller/database.py

#==== 啟動 controller.py =====
uv run controller/controller.py
