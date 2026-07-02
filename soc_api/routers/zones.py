from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/zones", tags=["zones"])


@router.get("")
async def get_zones():
    return {
        "zones": [
            {"zone_id": "ZONE-01", "alert_level": 0, "device_count": 342,
             "active_alerts": 0, "status": "healthy"},
            {"zone_id": "ZONE-04", "alert_level": 1, "device_count": 398,
             "active_alerts": 2, "status": "elevated"},
        ]
    }


@router.get("/{zone_id}")
async def get_zone(zone_id: str):
    return {"zone_id": zone_id, "alert_level": 0, "device_count": 342, "active_alerts": 0}


@router.get("/model-versions")
async def get_model_versions():
    return {
        "zones": [
            {"zone_id": "ZONE-01", "model_version": "global-v47"},
            {"zone_id": "ZONE-04", "model_version": "global-v47"},
        ]
    }
