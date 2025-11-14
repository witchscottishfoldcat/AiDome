# core/decision_maker.py

import logging

from app.event_bus import event_bus
from schemas.events import SendWebSocketMessageEvent, StateChangedEvent, WebSocketMessageReceivedEvent
from services.memory_service import memory_service
# --- 【核心变更】 ---
# 导入我们新创建的LLM服务
from services.llm_service import llm_service

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
        
        业务逻辑：现在，决策将构建一个Prompt并调用LLM服务。
        """
        current_state = event.current_state
        
        recent_memories = await memory_service.get_recent_memories(limit=1)
        last_memory_content = "nothing in particular"
        if recent_memories:
            last_memory_content = recent_memories[0].content

        # --- 【核心变更】: 构建动态Prompt ---
        # 我们不再使用if/else来拼接字符串，而是创建一个丰富的上下文Prompt。
        prompt = f"""
        你是一个AI桌面宠物。请根据你的当前状态和最近的记忆，生成一句简短、符合你身份的回应。

        # 你的当前状态:
        - 能量 (Energy): {current_state.energy:.2f} / 100.0

        # 最近发生的事 (Memory):
        - {last_memory_content}

        请直接生成回应，不要包含任何前缀或解释。
        """
        
        # --- 【核心变更】: 调用LLM服务 ---
        # 将决策的“创造性”部分外包给LLM。
        response_text = await llm_service.generate_response(prompt)
        
        response_payload = {
            "command_name": "show_dialogue",
            "payload": {"text": response_text}
        }
        
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

decision_maker = DecisionMaker()