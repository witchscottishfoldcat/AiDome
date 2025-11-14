# core/state_manager.py
import logging

from app.event_bus import event_bus
from schemas.events import StateChangedEvent, WebSocketMessageReceivedEvent
from schemas.state import PetState  # 【变更】从新的位置导入

logger = logging.getLogger("ArkHeart.Core.StateManager")

# --- 3. 实现状态管理器 ---
# 这是一个单例类，确保整个应用中只有一个状态源。
class StateManager:
    """管理PetState的生命周期，并响应事件来更新状态。"""
    _instance = None
    state: PetState

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化时，为宠物创建一个初始状态实例。
            cls._instance.state = PetState()
            logger.info(f"StateManager initialized with initial state: {cls._instance.state}")
        return cls._instance

    async def setup_subscriptions(self):
        await event_bus.subscribe(WebSocketMessageReceivedEvent, self._handle_message_received)
        logger.info("StateManager has subscribed to relevant events.")

    async def _handle_message_received(self, event: WebSocketMessageReceivedEvent):
        energy_cost = 0.5
        previous_energy = self.state.energy
        self.state.energy = max(0.0, self.state.energy - energy_cost)
        
        reason_for_change = f"Message received from {event.client_id}"
        logger.info(
            f"Energy changed: {previous_energy:.2f} -> {self.state.energy:.2f} "
            f"(Reason: {reason_for_change})"
        )

        # --- 【核心变更】 ---
        # 状态更新后，立即发布一个 StateChangedEvent
        await event_bus.publish(
            StateChangedEvent(
                current_state=self.state,
                reason=reason_for_change
            )
        )

# 创建全局实例
state_manager = StateManager()