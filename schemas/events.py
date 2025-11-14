# schemas/events.py

from abc import ABC
from dataclasses import dataclass, field, KW_ONLY
from datetime import datetime
from typing import TypeVar
from uuid import UUID, uuid4
from .state import PetState
from typing import Any, Dict
from typing import Optional
# --- 1. 事件的抽象基类 ---
# 这是系统中所有事件的“父类”，定义了它们的共同结构。
@dataclass(kw_only=True)
class BaseEvent(ABC):
    timestamp: datetime = field(default_factory=datetime.utcnow, repr=False)
    event_id: UUID = field(default_factory=uuid4, repr=False)
    priority: int = 1

# --- 2. 用于类型提示的泛型 ---
# 这确保了我们的事件总线在订阅时是类型安全的。
T = TypeVar("T", bound=BaseEvent)

# --- 3. 具体的输入事件定义 ---
# 未来所有从外部输入转化而来的事件都将定义在此处。
@dataclass
class WebSocketMessageReceivedEvent(BaseEvent):
    """当从WebSocket客户端收到一条消息时触发的事件。"""
    client_id: str
    message_text: str

@dataclass
class StateChangedEvent(BaseEvent):
    """当宠物的核心状态发生任何变化时发布。"""
    current_state: PetState
    reason: str
    # 【核心变更】添加一个可选字段来携带触发源事件
    trigger_event: Optional[BaseEvent] = None
    
# --- 4. 具体的输出/指令事件定义 ---
# 未来所有由“大脑”内部发出，指令外部模块执行的事件都将定义在此处。
@dataclass
class SendWebSocketMessageEvent(BaseEvent):
    """指令一个IO模块向指定的客户端发送一条WebSocket消息。"""
    client_id: str
    payload: Dict[str, Any]