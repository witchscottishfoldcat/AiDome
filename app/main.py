# app/main.py
import logging

from fastapi import FastAPI

from core.state_manager import state_manager
from schemas.events import StateChangedEvent
from schemas.state import PetState
from app.event_bus import event_bus
# WebSocket相关的导入暂时保留，因为endpoint还需要
from app.websocket_handler import setup_websocket_handler 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ArkHeart.Brain.Main")

# --- 【新】临时的状态变化日志记录器 ---
async def log_state_changes(event: StateChangedEvent):
    logger.info(
        f"[State Logger] Pet state changed! New energy: {event.current_state.energy:.2f}. "
        f"Reason: {event.reason}"
    )

app = FastAPI(title="ArkHeart Brain Service", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    await state_manager.setup_subscriptions()
    
    # --- 【核心变更】 ---
    # 订阅我们新创建的 StateChangedEvent
    await event_bus.subscribe(StateChangedEvent, log_state_changes)
    logger.info("State change logger subscribed.")

# --- 【变更】将WebSocket逻辑移出 ---
# 我们将在下一步中将WebSocket逻辑分离到一个专门的文件中
setup_websocket_handler(app)

@app.get("/")
async def read_root():
    return {"status": "ArkHeart Brain is alive and listening."}