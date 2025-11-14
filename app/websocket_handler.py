# app/websocket_handler.py
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from schemas.events import WebSocketMessageReceivedEvent
from app.event_bus import event_bus

logger = logging.getLogger("ArkHeart.Brain.WebSocket")

async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info(f"Connection established with client: {client_id}")
    try:
        await websocket.send_json({
            "command_name": "handshake_response",
            "payload": {"accepted": True, "server_version": "0.1.0"} # 暂时硬编码
        })
        while True:
            received_data = await websocket.receive_text()
            logger.debug(f"Raw data received from {client_id}: {received_data}")
            await event_bus.publish(
                WebSocketMessageReceivedEvent(client_id=client_id, message_text=received_data)
            )
    except WebSocketDisconnect:
        logger.warning(f"Client {client_id} has disconnected.")
    except Exception as e:
        logger.error(f"An unexpected error occurred with client {client_id}: {e}", exc_info=True)

def setup_websocket_handler(app: FastAPI):
    app.add_api_websocket_route("/ws/v1/{client_id}", websocket_endpoint)