#!/usr/bin/env python3
"""
警報歷史 API 路由
提供警報歷史查詢、統計等功能
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

from server.core import get_db_manager, manager
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

# 定義請求和回應模型
class AlertNotificationRequest(BaseModel):
    """警報通知請求模型"""
    alert_type: str
    severity: str
    message: str
    timestamp: str
    sensor_data: Dict[str, Any]

class AlertResponse(BaseModel):
    """警報資料回應模型"""
    id: int
    alert_type: str
    severity: str
    message: str
    sensor_data: str
    timestamp: str
    sent_to_frontend: bool
    created_at: str

class AlertListResponse(BaseModel):
    """警報列表回應模型"""
    status: str = "success"
    data: List[AlertResponse]
    count: int
    limit: Optional[int] = None
    offset: Optional[int] = None

class AlertStatisticsResponse(BaseModel):
    """警報統計回應模型"""
    status: str = "success"
    data: Dict[str, Any]

# API 路由
@router.post("/notify")
async def notify_alert(alert: AlertNotificationRequest):
    """
    接收來自 Controller 的警報通知
    
    參數:
    - alert: 警報通知資料
    """
    # 驗證警報類型
    valid_alert_types = ["high_temperature", "low_humidity"]
    if alert.alert_type not in valid_alert_types:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": {
                    "message": f"無效的警報類型。有效類型: {', '.join(valid_alert_types)}"
                }
            }
        )
    
    # 驗證嚴重程度
    valid_severities = ["info", "warning", "error"]
    if alert.severity not in valid_severities:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": {
                    "message": f"無效的嚴重程度。有效程度: {', '.join(valid_severities)}"
                }
            }
        )
    
    # 實作 WebSocket 推播功能
    # 將警報推播給所有連線的前端客戶端
    try:
        await manager.broadcast_alert({
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "timestamp": alert.timestamp,
            "sensor_data": alert.sensor_data
        })
        print(f"✅ 警報已推播: {alert.alert_type} - {alert.message}")
    except Exception as e:
        print(f"❌ WebSocket 推播失敗: {e}")
        # 即使推播失敗，仍然回傳成功（因為警報已被接收）
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "警報通知已接收並推播"
        }
    )

@router.get("/history", response_model=AlertListResponse)
async def get_alert_history(
    alert_type: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
) -> AlertListResponse:
    """
    取得警報歷史列表
    
    參數:
    - alert_type: 警報類型過濾
    - severity: 嚴重程度過濾
    - limit: 回傳筆數限制
    - offset: 分頁偏移量
    """
    # 驗證警報類型
    valid_alert_types = ["high_temperature", "low_humidity"]
    if alert_type and alert_type not in valid_alert_types:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"無效的警報類型。有效類型: {', '.join(valid_alert_types)}"
            }
        )
    
    # 驗證嚴重程度
    valid_severities = ["info", "warning", "error"]
    if severity and severity not in valid_severities:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"無效的嚴重程度。有效程度: {', '.join(valid_severities)}"
            }
        )
    
    db = get_db_manager()
    alerts, total_count = db.get_alert_history(
        limit=limit,
        offset=offset,
        alert_type=alert_type,
        severity=severity
    )
    
    return AlertListResponse(
        data=alerts,
        count=total_count,
        limit=limit,
        offset=offset
    )

@router.get("/history/range", response_model=AlertListResponse)
async def get_alert_history_by_date_range(
    start_date: str,
    end_date: str,
    alert_type: Optional[str] = None,
    severity: Optional[str] = None
) -> AlertListResponse:
    """
    根據日期範圍取得警報歷史
    
    參數:
    - start_date: 開始日期 (YYYY-MM-DD)
    - end_date: 結束日期 (YYYY-MM-DD)
    - alert_type: 警報類型過濾
    - severity: 嚴重程度過濾
    """
    try:
        # 驗證日期格式
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
        
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "message": "開始日期不能晚於結束日期"
                }
            )
            
        db = get_db_manager()
        alerts, total_count = db.get_alert_history_by_date_range(
            start_date=start_date,
            end_date=end_date,
            alert_type=alert_type,
            severity=severity
        )
        
        return AlertListResponse(
            data=alerts,
            count=total_count
        )
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "日期格式錯誤，請使用 YYYY-MM-DD 格式"
            }
        )

@router.get("/statistics", response_model=AlertStatisticsResponse)
async def get_alert_statistics() -> AlertStatisticsResponse:
    """
    取得警報統計資訊
    
    回傳:
    - total_alerts: 總警報數
    - alerts_by_type: 依類型統計
    - alerts_by_severity: 依嚴重程度統計
    - alerts_last_24h: 最近 24 小時警報數
    - latest_alert_time: 最新警報時間
    """
    db = get_db_manager()
    stats = db.get_alert_statistics()
    return AlertStatisticsResponse(data=stats)

# 移除 handle_error 函數，直接使用 HTTPException
