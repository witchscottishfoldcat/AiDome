# app/websocket_handler.py

import logging
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from schemas.events import SendWebSocketMessageEvent, WebSocketMessageReceivedEvent
from app.event_bus import event_bus

logger = logging.getLogger("ArkHeart.Brain.WebSocket")

class ConnectionManager:
    """管理所有活跃的WebSocket连接。"""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Connection established with client: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.warning(f"Client {client_id} has disconnected.")

    async def send_to_client(self, client_id: str, payload: dict):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(payload)
            logger.info(f"Message sent to {client_id}: {payload}")
        else:
            logger.error(f"Attempted to send message to disconnected client: {client_id}")

manager = ConnectionManager()

async def handle_send_message_command(event: SendWebSocketMessageEvent):
    """事件处理器：执行发送WebSocket消息的指令。"""
    await manager.send_to_client(event.client_id, event.payload)

async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        await manager.send_to_client(client_id, {
            "command_name": "handshake_response",
            "payload": {"accepted": True, "server_version": "0.1.0"}
        })
        while True:
            received_data = await websocket.receive_text()
            logger.debug(f"Raw data received from {client_id}: {received_data}")
            await event_bus.publish(
                WebSocketMessageReceivedEvent(client_id=client_id, message_text=received_data)
            )
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"An unexpected error occurred with client {client_id}: {e}", exc_info=True)
        manager.disconnect(client_id)

def setup_websocket_handler(app: FastAPI):
    app.add_api_websocket_route("/ws/v1/{client_id}", websocket_endpoint)