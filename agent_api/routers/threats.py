from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1/threats", tags=["threats"])

_threats_db = []


@router.get("")
async def get_threats(
    zone_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    threat_class: Optional[str] = Query(None),
    since: Optional[str] = Query(None),
    limit: int = Query(50, le=500),
    offset: int = Query(0),
):
    results = _threats_db[::-1]
    if zone_id:
        results = [r for r in results if r.get("zone_id") == zone_id]
    if status:
        results = [r for r in results if r.get("status") == status]
    if threat_class:
        results = [r for r in results if r.get("threat_class") == threat_class]
    return {"total": len(results), "page": offset // limit + 1, "results": results[offset:offset + limit]}


@router.post("/{incident_id}/review")
async def review_threat(incident_id: str, body: dict):
    for inc in _threats_db:
        if inc.get("incident_id") == incident_id:
            action = body.get("action", "")
            if action == "CONFIRM":
                inc["status"] = "CONFIRMED"
            elif action == "FALSE_POSITIVE":
                inc["status"] = "FALSE_POSITIVE"
                inc["false_positive_confirmed"] = True
            elif action == "RELEASE":
                inc["status"] = "RESOLVED"
            inc["operator_notes"] = body.get("notes", "")
            inc["operator_id"] = body.get("operator_id", "")
            return {"incident_id": incident_id, "status": inc["status"],
                    "updated_at": "2025-01-15T08:45:00Z"}
    return {"error": "Incident not found"}
