# 📜 Schemas: The Universal Language & Data Contracts

本目录是“方舟之心”项目的**“通用语言”定义中心**。它包含了所有用于系统内部和外部通信的**数据结构（“契约”）**。遵循严格的、类型安全的数据模式，是我们实现健壮、可维护、解耦架构的基石。

**核心原则：** 任何跨越模块边界的数据传递，**都必须**使用本目录中定义的Pydantic模型或Dataclass对象。**严禁**使用原始的`dict`在模块间传递复杂数据。

---

## 模块职责与核心文件 (Module Responsibilities)

### `events.py` (The Internal Nervous System's Signals)

- **职责:** **[大脑内部的“法律”]** 使用Python的`dataclasses`，定义了所有在**内部事件总线 (`Event Bus`)**上传递的事件。
- **设计哲学:**
    - **面向逻辑:** 这里的每一个事件类（如`UserSaidSomethingEvent`, `StateChangedEvent`）都代表了一个**高层次的、有业务逻辑含义**的内部信号。
    - **丰富上下文:** 事件对象被设计为携带丰富的上下文信息（如`full_context_snapshot`），以便订阅者（如`DecisionMaker`）能获得做出决策所需的全部信息。
    - **Python原生:** 使用`dataclasses`能获得最佳的性能和与Python类型提示系统的集成。
- **示例:** `StateChangedEvent`携带了完整的`previous_state`和`current_state`快照，这对于需要对“变化”做出反应的模块来说，是至关重要的上下文。

### `api_models.py` (The Diplomatic Language for the Outside World)

- **职责:** **[与“身体”沟通的“法律”]** 使用**Pydantic**模型，定义了所有通过**WebSocket**在“大脑”和“身体”之间传递的JSON消息的**结构、类型和验证规则**。
- **设计哲学:**
    - **面向通信:** 这里的每一个模型（如`WebSocketRequest`, `PlayAnimationPayload`）都精确地、一对一地映射了一个**网络上传输的JSON对象**。
    - **数据验证:** Pydantic的强大之处在于它能在数据**进入**系统（反序列化）和**离开**系统（序列化）的边界，进行**严格的数据验证**。如果“身体”发送了一个格式错误的消息，它会在`api/`层就被Pydantic捕获并拒绝，而不会污染到我们的`core/`核心逻辑。
    - **JSON友好:** Pydantic模型能轻松地与JSON进行相互转换 (`.model_dump_json()`, `.model_parse_json()`)，并能自动生成符合OpenAPI/AsyncAPI规范的Schema。

## 工作流：一个请求的数据形态变换 (Data Transformation Workflow)

理解这两个文件的区别，最好的方式是追踪一次“用户点击”的数据流：

1.  **“身体” (Frontend):** 捕捉到点击，构建一个JSON对象：
    `{ "event_name": "user_interaction", "payload": { "type": "touch", ... } }`

2.  **`api/endpoints/websocket.py`:**
    - 接收到JSON字符串。
    - 使用`api_models.py`中的`WebSocketRequest`模型对其进行**解析和验证**：`req = WebSocketRequest.model_validate_json(raw_data)`。如果验证失败，立即向客户端返回错误。

3.  **`services/websocket_service.py`:**
    - 从`req`对象中提取出`payload`数据。
    - **“翻译”:** 将这个面向通信的Pydantic模型，**转换**为一个面向内部逻辑的`dataclass`事件：`event = UserInteractedEvent(interaction_type="touch", data=req.payload.data)`。
    - **发布:** 调用 `event_bus.publish(event)`。

4.  **`core/`模块:** `DecisionMaker`等模块**只**订阅和处理`schemas/events.py`中定义的、干净的、经过验证的内部事件对象。

## 如何扩展数据契约？ (How to Extend the Data Contracts)

### 添加一个新的“内部事件”：
1.  **定义:** 在`schemas/events.py`中，创建一个新的`@dataclass`，并继承自`BaseEvent`。
2.  **使用:** 在需要发布该事件的模块（发布者）中，导入并实例化它。在需要响应的模块（订阅者）中，导入它的类型并进行订阅。

### 为“大脑-身体”通信添加一个新的消息类型：
1.  **定义 (双方):**
    - **首先，**在**`附录B`**中，为这个新消息添加一行，定义其`event_name`和`payload`结构。这是“唯一真理”。
    - **然后，**在`schemas/api_models.py`中，创建一个新的Pydantic模型来精确地描述这个`payload`。
2.  **实现 (后端):**
    - 在`api/endpoints/websocket.py`的接收逻辑中，增加一个`case`来处理这个新的`event_name`。
    - 如果需要，在`schemas/events.py`中创建一个对应的内部事件，并在`WebSocketService`中进行“翻译”。
3.  **实现 (前端):** “身体”的`WebSocketClient`中，增加发送或接收这个新消息的逻辑。

---