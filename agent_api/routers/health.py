from fastapi import APIRouter, Depends
from typing import Optional

router = APIRouter(tags=["health"])


@router.get("/api/v1/health")
async def get_health():
    return {
        "status": "ok",
        "zone_id": "ZONE-04",
        "uptime_seconds": 86400,
        "devices_monitored": 342,
        "model_version": "global-v47",
        "last_fl_round": "2025-01-15T07:00:00Z",
        "kafka_lag_messages": 3,
        "inference_latency_ms_p99": 187,
    }
