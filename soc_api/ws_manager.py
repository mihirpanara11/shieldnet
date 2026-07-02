from typing import Set, Dict
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger("shieldnet.soc.ws")


class WebSocketManager:
    def __init__(self):
        self._connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._connections.add(websocket)
        logger.info(f"WebSocket client connected ({len(self._connections)} total)")

    def disconnect(self, websocket: WebSocket):
        self._connections.discard(websocket)
        logger.info(f"WebSocket client disconnected ({len(self._connections)} total)")

    async def broadcast(self, event: str, data: dict):
        message = json.dumps({"event": event, "data": data})
        dead = set()
        for ws in self._connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._connections.discard(ws)

    async def broadcast_threat(self, incident: dict):
        await self.broadcast("NEW_THREAT", incident)

    async def broadcast_airo_action(self, incident_id: str, action: str, status: str):
        await self.broadcast("AIRO_ACTION", {
            "incident_id": incident_id,
            "action": action,
            "status": status,
        })

    async def broadcast_zone_status(self, zone_id: str, alert_level: int):
        await self.broadcast("ZONE_STATUS_CHANGE", {
            "zone_id": zone_id,
            "alert_level": alert_level,
        })

    async def broadcast_device_restored(self, device_id: str, incident_id: str):
        await self.broadcast("DEVICE_RESTORED", {
            "device_id": device_id,
            "incident_id": incident_id,
        })

    @property
    def connection_count(self) -> int:
        return len(self._connections)
