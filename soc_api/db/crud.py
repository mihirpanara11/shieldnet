from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from soc_api.db.models import Incident, DeviceProfile, PlaybookExecution, OperatorAction


class IncidentCRUD:
    @staticmethod
    async def create(db: AsyncSession, incident: dict) -> Incident:
        db_incident = Incident(
            incident_ref=incident.get("incident_id", ""),
            detected_at=datetime.now(),
            zone_id=incident.get("zone_id", ""),
            device_category=incident.get("device_category", ""),
            threat_class=incident.get("threat_class", ""),
            confidence_score=incident.get("confidence_score", 0.0),
            status=incident.get("status", "ACTIVE"),
            actions_taken=incident.get("actions_taken"),
        )
        db.add(db_incident)
        await db.commit()
        await db.refresh(db_incident)
        return db_incident

    @staticmethod
    async def get_all(db: AsyncSession, zone_id: Optional[str] = None,
                      status: Optional[str] = None,
                      threat_class: Optional[str] = None,
                      limit: int = 50, offset: int = 0) -> List[Incident]:
        query = select(Incident)
        if zone_id:
            query = query.where(Incident.zone_id == zone_id)
        if status:
            query = query.where(Incident.status == status)
        if threat_class:
            query = query.where(Incident.threat_class == threat_class)
        query = query.order_by(Incident.detected_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count(db: AsyncSession, zone_id: Optional[str] = None,
                    status: Optional[str] = None) -> int:
        query = select(func.count(Incident.id))
        if zone_id:
            query = query.where(Incident.zone_id == zone_id)
        if status:
            query = query.where(Incident.status == status)
        result = await db.execute(query)
        return result.scalar()

    @staticmethod
    async def get_by_id(db: AsyncSession, incident_id: str) -> Optional[Incident]:
        query = select(Incident).where(Incident.incident_ref == incident_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_status(db: AsyncSession, incident_id: str, status: str,
                            operator_id: Optional[str] = None,
                            notes: Optional[str] = None) -> Optional[Incident]:
        incident = await IncidentCRUD.get_by_id(db, incident_id)
        if incident:
            incident.status = status
            if operator_id:
                incident.operator_id = operator_id
            if notes:
                incident.operator_notes = notes
            await db.commit()
            await db.refresh(incident)
        return incident
