from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])


@router.get("")
async def get_incidents(
    zone_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    threat_class: Optional[str] = Query(None),
    limit: int = Query(50, le=500),
    offset: int = Query(0),
):
    return {"total": 0, "page": offset // limit + 1, "results": []}


@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    return {"incident_id": incident_id, "status": "ACTIVE"}


@router.get("/{incident_id}/export")
async def export_incident(incident_id: str, format: str = "pdf"):
    return {"incident_id": incident_id, "format": format, "url": f"/reports/{incident_id}.{format}"}
