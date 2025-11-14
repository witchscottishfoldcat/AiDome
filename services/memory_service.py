# services/memory_service.py

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.event_bus import event_bus
from schemas.events import WebSocketMessageReceivedEvent

logger = logging.getLogger("ArkHeart.Services.Memory")

# --- 1. 定义记忆的数据结构 ---
@dataclass
class MemoryItem:
    """代表一条记忆。"""
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    importance: float = 0.5  # 记忆重要性，未来会用到
    
# --- 2. 定义记忆服务的“接口”（抽象基类） ---
# 这份“契约”规定了任何一个记忆服务都必须提供哪些功能。
class IMemoryService(ABC):
    """记忆服务的抽象接口。"""

    @abstractmethod
    async def add_memory(self, content: str):
        """添加一条新记忆。"""
        pass

    @abstractmethod
    async def get_recent_memories(self, limit: int) -> List[MemoryItem]:
        """获取最近的几条记忆。"""
        pass

    @abstractmethod
    async def setup_subscriptions(self):
        """将服务连接到事件总线。"""
        pass

# --- 3. 实现一个“内存中的”模拟记忆服务 ---
# 这个类实现了上面的接口，但它不依赖任何数据库或外部服务。
# 它将所有记忆都保存在一个Python列表中，程序关闭后记忆就会丢失。
# 这对于我们当前阶段的开发和测试来说是完美的。
class InMemoryMemoryService(IMemoryService):
    """
    一个基于内存列表的、用于开发和测试的模拟记忆服务。
    """
    def __init__(self):
        self._short_term_memory: List[MemoryItem] = []
        logger.info("InMemoryMemoryService initialized.")

    async def add_memory(self, content: str):
        memory_item = MemoryItem(content=content)
        self._short_term_memory.append(memory_item)
        logger.info(f"Added to short-term memory: '{memory_item.content}'")
        # 保持一个合理的内存大小，防止无限增长
        if len(self._short_term_memory) > 20:
            self._short_term_memory.pop(0)

    async def get_recent_memories(self, limit: int) -> List[MemoryItem]:
        # 返回列表的最后 N 个元素
        recent = self._short_term_memory[-limit:]
        logger.info(f"Retrieved {len(recent)} recent memories.")
        return recent

    async def setup_subscriptions(self):
        """订阅用户对话事件，并将其内容存为记忆。"""
        await event_bus.subscribe(WebSocketMessageReceivedEvent, self._handle_user_speech)
        logger.info("MemoryService has subscribed to relevant events.")

    async def _handle_user_speech(self, event: WebSocketMessageReceivedEvent):
        # 我们只将用户的对话内容存为记忆
        await self.add_memory(f"User said: {event.message_text}")

# --- 4. 导出单例实例 ---
# 在整个应用中，我们将使用这个模拟服务的实例。
memory_service: IMemoryService = InMemoryMemoryService()