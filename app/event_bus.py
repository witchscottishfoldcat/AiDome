# app/event_bus.py

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine, Dict, List, Type, DefaultDict

# --- 【核心变更】 ---
# 从我们集中的"法典"文件中导入事件基类和类型变量
from schemas.events import BaseEvent, T

logger = logging.getLogger("ArkHeart.EventBus")

HandlerCoroutine = Callable[[T], Coroutine[Any, Any, None]]

class EventBus:
    _instance = None
    _subscribers: DefaultDict[Type[BaseEvent], List[HandlerCoroutine]]
    _lock: asyncio.Lock

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = defaultdict(list)
            cls._instance._lock = asyncio.Lock()
        return cls._instance

    async def subscribe(self, event_type: Type[T], handler: HandlerCoroutine[T]):
        async with self._lock:
            self._subscribers[event_type].append(handler)
            logger.debug(f"Handler '{handler.__name__}' subscribed to event '{event_type.__name__}'")

    async def publish(self, event: BaseEvent):
        event_type = type(event)
        logger.info(f"Publishing event: {event_type.__name__} (ID: {event.event_id})")

        handlers = self._subscribers.get(event_type, [])
        if not handlers:
            logger.warning(f"No subscribers for event: {event_type.__name__}")
            return

        await asyncio.gather(*(handler(event) for handler in handlers))

event_bus = EventBus()