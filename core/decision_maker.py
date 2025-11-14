# core/decision_maker.py

import logging

from app.event_bus import event_bus
from schemas.events import SendWebSocketMessageEvent, StateChangedEvent, WebSocketMessageReceivedEvent
# --- 【核心变更】 ---
# 导入我们的记忆服务
from services.memory_service import memory_service

logger = logging.getLogger("ArkHeart.Core.DecisionMaker")

class DecisionMaker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.info("DecisionMaker initialized.")
        return cls._instance

    async def setup_subscriptions(self):
        await event_bus.subscribe(StateChangedEvent, self._on_state_changed)
        logger.info("DecisionMaker has subscribed to relevant events.")

    async def _on_state_changed(self, event: StateChangedEvent):
        """
        事件处理器：当宠物的状态发生变化时。

        业务逻辑：现在，决策会结合“当前状态”和“近期记忆”。
        """
        current_state = event.current_state
        
        # --- 【核心变更】: 查询记忆 ---
        # 在做决策前，先从记忆服务获取最近的一条记忆。
        recent_memories = await memory_service.get_recent_memories(limit=1)
        last_memory_content = "nothing in particular"
        if recent_memories:
            last_memory_content = recent_memories[0].content

        # --- 【核心变更】: 基于状态和记忆进行决策 ---
        # 决策逻辑现在更加丰富了。
        if current_state.energy > 50.0:
            response_text = (
                f"我感觉精力充沛 (能量: {current_state.energy:.2f})。 "
                f"我们刚才聊到 '{last_memory_content}', 对吧？"
            )
        else:
            response_text = (
                f"有点累了... (能量: {current_state.energy:.2f})。 "
                f"我记得你说过 '{last_memory_content}', 但我现在需要休息一下。"
            )
            
        response_payload = {
            "command_name": "show_dialogue",
            "payload": {"text": response_text}
        }
        
        # 从 trigger_event 中安全地获取 client_id
        client_id = None
        if event.trigger_event and isinstance(event.trigger_event, WebSocketMessageReceivedEvent):
            client_id = event.trigger_event.client_id
        
        if client_id:
             await event_bus.publish(
                 SendWebSocketMessageEvent(
                     client_id=client_id,
                     payload=response_payload
                 )
             )
        else:
            logger.debug("State changed without a specific client context. No message sent.")

# 导出单例
decision_maker = DecisionMaker()