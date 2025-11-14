# 🧠 Core: The AI's Mind and Soul

**警告：本目录包含了“方舟之心”项目最核心、最复杂的AI心智逻辑。任何对此处代码的修改，都可能深刻地、非预期地改变宠物的性格与行为。在进行修改前，请确保您已完全理解《创世设计文档》中的[第四章(人格系统)](link)和[第五章(决策逻辑)](link)。**

本模块的职责是模拟一个完整的“**思考-感知**”循环，它是宠物“灵魂”的所在地。

---

## 模块职责与核心文件 (Module Responsibilities)

- **`state_manager.py` (The Heart & Soul):**
    - **职责:** 作为宠物**内在状态（L1）**和**性格特质（L2）**的“唯一真理之源”。
    - **工作模式:** 订阅`SystemTickEvent`和所有相关交互事件，根据《创世设计文档》中定义的**心理学和行为逻辑学算法**，独立地、持续地计算和更新宠物的状态（能量、情感、饱和度等）。当状态变化时，发布`StateChangedEvent`。

- **`decision_maker.py` (The Cortex):**
    - **职责:** 整个AI的**“总导演”和“决策中枢”**。
    - **工作模式:** 这是一个高度复杂的模块，它订阅了系统中的**大部分核心事件**（如`UserSaidSomethingEvent`, `StateChangedEvent`）。当被触发时，它会协调`services`模块获取所需信息（如记忆），并根据当前状态和长期目标，**构建动态Prompt**，最终决定是调用LLM、执行技能还是直接做出反应。

- **`mental_immune_system.py` (The Guardian & Psychologist):**
    - **职责:** 作为更高维度的“守护进程”，保障AI心智的**长期健康与一致性**。
    - **工作模式:**
        - **`Guardian`:** 通过监听行为事件流，防止宠物陷入**行为循环（卡死）**。
        - **`Psychologist`:** 在LLM输出后进行拦截，通过“AI监督AI”的方式，防止**人格漂移（OOC）**。

- **`exception_handler.py` (The Pain Reflex):**
    - **职责:** 实现“**叙事化错误处理**”。
    - **工作模式:** 订阅`ExceptionOccurredEvent`，将冰冷的技术错误（如`APITimeoutError`）**翻译**为符合宠物人设的**内在情感状态变化**（如`[FRUSTRATED]`），从而驱动一次“有故事”的失败表演。

## “心跳”工作流：一个事件的旅程 (The Heartbeat Workflow)

理解本模块的关键，在于理解一个事件是如何在其中流转的。以“用户说话”为例：

1.  **`UserSaidSomethingEvent`** 由`WebSocketService`发布到**事件总线**。
2.  **`DecisionMaker`** 作为订阅者被激活。
3.  `DecisionMaker`**并行**地：
    - 从`StateManager`获取**当前情绪和状态**的快照。
    - 向`MemoryService`发布`RetrieveMemoryEvent`，请求相关记忆。
4.  `MemoryService`在完成后，发布`MemoryRetrievedEvent`。
5.  `DecisionMaker`再次被激活，此时它已集齐所有上下文（用户输入、当前状态、历史记忆）。
6.  它执行**“元认知”**和**“决策优先级”**判断，然后**构建最终的Prompt**。
7.  它向`LLMService`发布`InvokeLLMEvent`。
8.  `LLMService`流式地发布`LLMStreamTokenEvent`。
9.  `Psychologist`模块会监听这些Token，并在流结束后进行**OOC评估**。
10. 如果一切正常，`WebSocketService`（作为`LLMStreamTokenEvent`的订阅者）会将Token实时转发给“身体”。

## 如何扩展AI的心智？ (How to Extend the AI's Mind)

### 修改或增加一个新的“内在状态”：
1.  **定义:** 在`config/default_config.yaml`和`附录C`中，定义新的参数（例如，`boredom` - 无聊度）。
2.  **实现:** 在**`state_manager.py`**中，增加计算该参数变化的逻辑（例如，长时间无新奇事件则`boredom`增加）。
3.  **应用:** 在**`decision_maker.py`**中，将`boredom`作为一个新的上下文，注入到Prompt中，或用它来驱动新的自主行为（例如，当`boredom`很高时，宠物会自己“找事做”）。

### 调整一个决策逻辑：
- **警告：这是最高风险的操作。**
1.  **定位:** 在**`decision_maker.py`**中，找到处理相关事件的函数。
2.  **测试优先:** 在`tests/core/test_decision_maker.py`中，编写一个**能够复现你想要改变的行为**的测试用例。
3.  **修改:** 小心翼翼地修改决策逻辑或Prompt构建过程。
4.  **验证:** 确保你修改后的代码，不仅通过了新的测试，也**没有破坏**任何已有的测试。

---