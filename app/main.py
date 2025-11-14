# app/main.py

import logging

from fastapi import FastAPI

from core.decision_maker import decision_maker
from core.state_manager import state_manager
# --- 【核心变更】 ---
# 导入我们的记忆服务
from services.memory_service import memory_service
from schemas.events import SendWebSocketMessageEvent
from app.event_bus import event_bus
from app.websocket_handler import handle_send_message_command, setup_websocket_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ArkHeart.Brain.Main")

app = FastAPI(title="ArkHeart Brain Service", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    
    # 激活核心模块
    await state_manager.setup_subscriptions()
    await decision_maker.setup_subscriptions()
    # --- 【核心变更】 ---
    # 激活记忆服务，让它开始订阅事件并记录记忆
    await memory_service.setup_subscriptions()
    
    # 订阅指令事件
    await event_bus.subscribe(SendWebSocketMessageEvent, handle_send_message_command)
    logger.info("All modules initialized and subscribed.")

# 设置网络接口
setup_websocket_handler(app)

@app.get("/")
async def read_root():
    return {"status": "ArkHeart Brain is alive and listening."}