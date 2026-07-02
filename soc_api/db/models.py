from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_ref = Column(String(30), unique=True, nullable=False)
    detected_at = Column(DateTime(timezone=True), nullable=False)
    contained_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    containment_time_ms = Column(Integer, nullable=True)
    zone_id = Column(String(20), nullable=False)
    device_category = Column(String(30), nullable=False)
    threat_class = Column(String(30), nullable=False)
    confidence_score = Column(Float, nullable=False)
    score_lstm = Column(Float, nullable=True)
    score_isolation_forest = Column(Float, nullable=True)
    score_autoencoder = Column(Float, nullable=True)
    playbook_id = Column(String(50), nullable=True)
    actions_taken = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")
    false_positive = Column(Boolean, default=False)
    operator_id = Column(String(50), nullable=True)
    operator_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DeviceProfile(Base):
    __tablename__ = "device_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String(30), unique=True, nullable=False)
    zone_id = Column(String(20), nullable=False)
    category = Column(String(30), nullable=False)
    protocol = Column(String(20), nullable=False)
    baseline_established = Column(Boolean, default=False)
    baseline_created_at = Column(DateTime(timezone=True), nullable=True)
    baseline_updated_at = Column(DateTime(timezone=True), nullable=True)
    firmware_updated_at = Column(DateTime(timezone=True), nullable=True)
    is_quarantined = Column(Boolean, default=False)
    quarantine_reason = Column(Text, nullable=True)
    alert_count_total = Column(Integer, default=0)
    alert_count_7d = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlaybookExecution(Base):
    __tablename__ = "playbook_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=True)
    playbook_id = Column(String(50), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    steps = Column(JSON, nullable=False)
    success = Column(Boolean, nullable=True)
    error_message = Column(Text, nullable=True)


class OperatorAction(Base):
    __tablename__ = "operator_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_id = Column(String(50), nullable=False)
    action_type = Column(String(50), nullable=False)
    target_type = Column(String(30), nullable=True)
    target_id = Column(String(50), nullable=True)
    payload = Column(JSON, nullable=True)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45), nullable=True)
    session_id = Column(String(100), nullable=True)
