# app/main.py

import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# --- 【核心变更】 ---
# 导入我们新创建的状态管理器
from core.state_manager import state_manager
from schemas.events import WebSocketMessageReceivedEvent
from .event_bus import event_bus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ArkHeart.Brain.Main")

# --- 【变更】 ---
# 我们不再需要临时的事件处理器，StateManager 将接管这个职责。
# async def handle_websocket_message(event: WebSocketMessageReceivedEvent):
#     logger.info(f"[EventHandler] Received message from '{event.client_id}': '{event.message_text}'")

app = FastAPI(title="ArkHeart Brain Service", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    """
    应用启动时，初始化并连接所有核心模块。
    """
    logger.info("Application starting up...")
    
    # --- 【核心变更】 ---
    # 激活状态管理器，让它去订阅自己关心的事件。
    await state_manager.setup_subscriptions()
    
    # 我们之前的临时订阅可以移除了。
    # await event_bus.subscribe(WebSocketMessageReceivedEvent, handle_websocket_message)
    # logger.info("Event handlers subscribed.")

@app.websocket("/ws/v1/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info(f"Connection established with client: {client_id}")
    try:
        await websocket.send_json({
            "command_name": "handshake_response",
            "payload": {"accepted": True, "server_version": app.version}
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

@app.get("/")
async def read_root():
    return {"status": "ArkHeart Brain is alive and listening."}