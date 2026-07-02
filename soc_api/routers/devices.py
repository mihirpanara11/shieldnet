from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


@router.get("")
async def get_devices(
    zone_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=500),
    offset: int = Query(0),
):
    return {"total": 0, "devices": []}


@router.get("/{device_id}")
async def get_device(device_id: str):
    return {
        "device_id": device_id,
        "status": "NORMAL",
        "anomaly_score_current": 0.12,
        "baseline_established": True,
    }
