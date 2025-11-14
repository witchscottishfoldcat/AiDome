# core/state_manager.py

import logging
from dataclasses import dataclass

# --- 1. 导入项目核心模块 ---
# StateManager 需要与事件总线和事件定义进行交互。
from app.event_bus import event_bus
from schemas.events import WebSocketMessageReceivedEvent

logger = logging.getLogger("ArkHeart.Core.StateManager")

# --- 2. 定义宠物的核心状态数据结构 ---
# 这是宠物所有内在状态的“容器”。
# 我们从GDD定义的最基础的L1层参数“能量”开始。
@dataclass
class PetState:
    """持有宠物所有实时、易变的内在状态参数。"""
    energy: float = 100.0  # 能量值，范围 0.0 - 100.0


# --- 3. 实现状态管理器 ---
# 这是一个单例类，确保整个应用中只有一个状态源。
class StateManager:
    """管理PetState的生命周期，并响应事件来更新状态。"""
    _instance = None
    # 显式声明state属性，解决basedpyright类型检查问题
    state: PetState

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化时，为宠物创建一个初始状态实例。
            cls._instance.state = PetState()
            logger.info(f"StateManager initialized with initial state: {cls._instance.state}")
        return cls._instance

    async def setup_subscriptions(self):
        """
        集中管理此模块所有的事件订阅。
        在应用启动时被调用，将状态管理器“连接”到事件总线。
        """
        await event_bus.subscribe(WebSocketMessageReceivedEvent, self._handle_message_received)
        logger.info("StateManager has subscribed to relevant events.")

    async def _handle_message_received(self, event: WebSocketMessageReceivedEvent):
        """
        事件处理器：当收到WebSocket消息时。

        业务逻辑：我们定义一个简单的规则 -> 每次与用户互动都会消耗一点精力。
        """
        # 定义每次交互消耗的能量值
        energy_cost = 0.5
        
        # 更新状态
        previous_energy = self.state.energy
        self.state.energy = max(0.0, self.state.energy - energy_cost) # 确保能量不会低于0
        
        # 打印日志以供观察，这是验证功能的核心
        logger.info(
            f"Energy changed: {previous_energy:.2f} -> {self.state.energy:.2f} "
            f"(Reason: Message received from {event.client_id})"
        )
        # 在未来，状态的重大变化会在这里发布一个新的`StateChangedEvent`。

# --- 4. 导出单例实例 ---
# 其他模块将导入这个实例来访问状态或调用方法。
state_manager = StateManager()