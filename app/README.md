# ⚡ App: The Heartbeat and Central Nervous System

本目录是“方舟之心”应用的**主入口和核心调度中心**。它负责实例化所有服务、装配整个应用，并提供了驱动所有模块异步协作的“**神经中枢**”——事件总线。

理解本目录下的`main.py`和`event_bus.py`，是理解整个“大脑”服务**如何“活”起来**的关键。

---

## 核心文件解析 (Core File Breakdown)

### `main.py`: The Grand Assembler

- **职责:**
    1.  **应用实例化:** 创建FastAPI的 app 实例。
    2.  **配置加载:** 在启动时，调用`config.loader`加载所有配置。
    3.  **依赖注入 (装配):** **[核心]** 调用`services/service_provider.py`，根据配置，创建所有核心模块和服务（`StateManager`, `DecisionMaker`, `LLMService`等）的**单例实例**。
    4.  **模块订阅:** 遍历所有已实例化的模块，并调用它们的`subscribe_to_events()`方法，将它们“挂载”到事件总线上。
    5.  **API路由挂载:** 将`api/`目录中定义的WebSocket和HTTP路由，挂载到FastAPI app上。
    6.  **后台任务启动:** 创建并启动`StateManager`的`SystemTickEvent`循环等常驻后台任务。

### `event_bus.py`: The Central Nervous System

- **职责:** 实现一个**全局唯一的、类型安全的、支持优先级的异步事件总线**。它是我们实现**极致解耦**的技术核心。
- **严禁直接调用此模块！** 所有模块都应通过依赖注入的方式，获取`EventBus`的实例。

---

## 核心设计模式：事件驱动架构 (EDA)

**本项目严禁模块间的直接方法调用！** 例如，`DecisionMaker`**永远不应该**写出`llm_service.invoke()`这样的代码。

### 为什么？ (The "Why")
- **解耦 (Decoupling):** 如果直接调用，`DecisionMaker`就与`LLMService`的具体实现**紧密耦合**了。未来更换`LLMService`，就可能需要修改`DecisionMaker`。
- **异步 (Asynchronicity):** 直接调用通常是阻塞的。事件驱动允许我们将耗时的任务（如API请求）“扔”到总线上，然后立刻去处理其他事情，不会阻塞主流程。
- **可观测性 (Observability):** 所有的系统活动，都被显式地、结构化地表达为“事件”。这使得我们可以轻易地在总线上加入日志、监控和调试的“探针”。

### 工作流 (The Workflow)

1.  **发布者 (Publisher):**
    - 一个模块（如`DecisionMaker`）想要执行一个动作。
    - 它会**实例化一个**在`schemas/events.py`中定义的、具体的事件对象（如`InvokeLLMEvent`）。
    - 然后调用 `await event_bus.publish(event)`。
    - **它的工作到此结束。** 它不关心谁会处理这个事件，也不关心何时处理完。

2.  **订阅者 (Subscriber):**
    - 另一个模块（如`LLMService`）在其初始化时，就已经向`EventBus`“注册”了它感兴趣的事件。
    - `event_bus.subscribe(InvokeLLMEvent, self.handle_llm_invocation)`
    - 当`InvokeLLMEvent`被发布时，`EventBus`会自动异步地调用`LLMService`的`handle_llm_invocation`方法，并将事件对象作为参数传入。

## 如何为系统添加新的“神经反射”？

假设你需要添加一个功能：当宠物能量过低时，自动向主人发送一条“我累了”的消息。

1.  **找到“触发器”:** 能量变化是由`StateManager`计算，并以`StateChangedEvent`的形式发布的。
2.  **创建“响应者”:** 你可以创建一个新的模块，或者在`DecisionMaker`中增加一个新的方法。

    ```python
    # In some_module.py
    
    class EnergyMonitor:
        def __init__(self, event_bus: EventBus):
            self._event_bus = event_bus
    
        async def handle_state_change(self, event: StateChangedEvent):
            # 检查是否是能量变化，并且低于阈值
            if "energy" in event.changed_params and event.current_state_snapshot['energy'] < 20:
                # 创建一个新的行为指令事件
                message_event = SendWebSocketMessageEvent(
                    command_name="show_notification",
                    payload={"message": "我好累呀，想睡觉了..."}
                )
                # 将新事件发布到总线
                await self._event_bus.publish(message_event)
        
        def subscribe_to_events(self):
            self._event_bus.subscribe(StateChangedEvent, self.handle_state_change)
    ```

3.  **“装配”:** 在`app/main.py`的启动逻辑中，实例化你的`EnergyMonitor`，并调用它的`subscribe_to_events()`方法。

**完成。** 你在**没有修改任何现有模块**的情况下，为系统增加了一条全新的、解耦的逻辑链路。这就是事件驱动架构的强大之处。

---