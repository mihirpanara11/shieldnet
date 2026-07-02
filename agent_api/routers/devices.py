from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])

_devices_db = []


@router.get("")
async def get_devices(
    zone_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=500),
    offset: int = Query(0),
):
    results = _devices_db
    if zone_id:
        results = [d for d in results if d.get("zone_id") == zone_id]
    if category:
        results = [d for d in results if d.get("category") == category]
    if status:
        results = [d for d in results if d.get("status") == status]
    return {"total": len(results), "devices": results[offset:offset + limit]}


@router.post("/enroll")
async def enroll_device(body: dict):
    device = {
        "device_id": f"DEV-{hash(body.get('device_mac', '')) % 10000:04d}",
        "category": body.get("category", "other"),
        "zone_id": body.get("zone_id", ""),
        "status": "ENROLLING",
        "protocol": body.get("protocol", "MQTT"),
        "firmware_version": body.get("firmware_version", "0.0.0"),
        "last_seen": "",
        "anomaly_score_current": 0.0,
        "baseline_established": False,
        "baseline_age_days": 0.0,
    }
    _devices_db.append(device)
    return device
