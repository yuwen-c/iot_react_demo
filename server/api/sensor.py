#!/usr/bin/env python3
"""
感測器相關的 API 端點
處理所有與感測器數據相關的請求
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any

from server.database import get_db_manager

# 建立路由器
router = APIRouter(
    prefix="/api/sensor",
    tags=["sensor"],
    responses={404: {"description": "Not found"}},
)

# 取得資料庫管理器
# 在 sensor.py 中的 get_db_manager() 呼叫不會建立新的實例，而是取得在 database.py 被導入時就已經建立的實例。
db_manager = get_db_manager()

@router.get("/latest")
async def get_latest_sensor_reading():
    """取得最新的感測器讀數"""
    try:
        reading = db_manager.get_latest_sensor_reading()
        if reading:
            return {
                "status": "success",
                "data": reading
            }
        else:
            raise HTTPException(status_code=404, detail="沒有找到感測器讀數")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得最新讀數失敗: {str(e)}")

@router.get("/readings")
async def get_sensor_readings(
    limit: int = Query(default=100, ge=1, le=1000, description="取得記錄數量"),
    offset: int = Query(default=0, ge=0, description="跳過的記錄數量")
):
    """取得感測器讀數列表"""
    try:
        readings = db_manager.get_sensor_readings(limit=limit, offset=offset)
        return {
            "status": "success",
            "data": readings,
            "count": len(readings),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得讀數列表失敗: {str(e)}")

@router.get("/readings/range")
async def get_sensor_readings_by_date_range(
    start_date: str = Query(..., description="開始日期 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="結束日期 (YYYY-MM-DD)")
):
    """根據日期範圍取得感測器讀數"""
    try:
        readings = db_manager.get_sensor_readings_by_date_range(start_date, end_date)
        return {
            "status": "success",
            "data": readings,
            "count": len(readings),
            "start_date": start_date,
            "end_date": end_date
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得日期範圍讀數失敗: {str(e)}")

@router.get("/statistics")
async def get_sensor_statistics():
    """取得感測器統計資訊"""
    try:
        stats = db_manager.get_sensor_statistics()
        if stats:
            return {
                "status": "success",
                "data": stats
            }
        else:
            raise HTTPException(status_code=404, detail="沒有找到統計資料")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得統計資訊失敗: {str(e)}")