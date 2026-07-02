from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from soc_api.ws_manager import WebSocketManager

router = APIRouter(tags=["websocket"])
ws_manager = WebSocketManager()


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)
