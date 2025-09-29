# dlp/api/endpoints/usb.py
from fastapi import APIRouter, HTTPException
from dlp.core.usb.monitor import usb_monitor
from datetime import datetime

router = APIRouter()

@router.get("/usb/status")
async def get_usb_status():
    return {
        "status": "active",
        "monitoring": usb_monitor.monitoring,
        "connected_devices": len(usb_monitor.connected_devices),
        "enterprise": True
    }

@router.get("/usb/devices")
async def get_usb_devices():
    return {
        "devices": usb_monitor.connected_devices,
        "count": len(usb_monitor.connected_devices),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/usb/history")
async def get_usb_history(limit: int = 10):
    history = usb_monitor.device_history[-limit:] if usb_monitor.device_history else []
    return {
        "events": history,
        "total_events": len(usb_monitor.device_history)
    }
