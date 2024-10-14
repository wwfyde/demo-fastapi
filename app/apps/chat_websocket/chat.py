from fastapi import APIRouter
from starlette.websockets import WebSocket

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, request_id: str, websocket: WebSocket):
        await websocket.accept()
        if request_id not in self.active_connections:
            self.active_connections[request_id] = []
        self.active_connections[request_id].append(websocket)

    def disconnect(self, request_id: str, websocket: WebSocket):
        self.active_connections[request_id].remove(websocket)
        if not self.active_connections[request_id]:
            del self.active_connections[request_id]

    async def broadcast(self, request_id: str, message: str):
        if request_id in self.active_connections:
            for connection in self.active_connections[request_id]:
                await connection.send_text(message)


manager = ConnectionManager()

# @router.websocket("/ws/progress/{request_id}")
