# 🔌 Services: The Senses and Voice of the Brain

本目录是“方舟之心”的**IO与外部服务适配层**。它的核心设计哲学是**“防腐层 (Anti-Corruption Layer)”**——将所有与外部世界（第三方API、本地服务、“身体”客户端）的通信细节，**完全封装和隔离**在此处。

**核心原则：** 系统的其他部分（特别是`core/`模块），**永远不应该知道**我们正在使用的是OpenAI还是Anthropic，是MemU还是其他记忆库。它们只与本目录在`interfaces.py`中定义的**抽象接口**对话。

---

## 模块职责与核心文件 (Module Responsibilities)

- **`interfaces.py` (The Contract):**
    - **职责:** **[本目录最重要的文件]** 使用Python的抽象基类(`abc`)，定义了所有IO服务的**“功能契约”**。例如，`ILLMService`接口定义了一个LLM服务**必须**提供`invoke()`等方法。
    - **意义:** 它是实现所有服务**可替换性**的技术基础。

- **`llm_service.py`, `tts_service.py`, `memory_service.py`, ... (The Implementations):**
    - **职责:** 提供一个或多个对`interfaces.py`中接口的**具体实现**。
    - **示例:**
        - `openai_llm_service.py` 实现了`ILLMService`，其内部逻辑是调用OpenAI的API。
        - `anthropic_llm_service.py` 也实现了`ILLMService`，其内部逻辑是调用Anthropic的API。

- **`service_provider.py` (The Factory - 新增建议):**
    - **职责:** 这是一个**依赖注入**的配置中心。它读取`config.yaml`中的配置，并根据配置，决定为系统**具体实例化**哪个服务的实现。
    - **示例逻辑:**
      ```python
      def get_llm_service() -> ILLMService:
          if config.services.llm.provider == "OpenAI":
              return OpenAILLMService()
          elif config.services.llm.provider == "Anthropic":
              return AnthropicLLMService()
          else:
              raise UnknownServiceProviderError()
      ```

## 扩展教程：如何更换LLM服务商 (Tutorial: How to Switch LLM Provider)

这是一个标准流程，展示了本架构的灵活性。假设我们要从OpenAI切换到Anthropic Claude。

### 步骤 1: 创建新的实现 (Create New Implementation)

在`services/`目录下，创建一个新文件`anthropic_llm_service.py`。

```python
# in services/anthropic_llm_service.py

from .interfaces import ILLMService

class AnthropicLLMService(ILLMService):
    def __init__(self):
        # 初始化Anthropic的客户端
        self.client = ...

    async def invoke(self, prompt: str, stream: bool) -> ...:
        # 编写调用Anthropic API的具体逻辑
        # 确保返回值与ILLMService接口定义的类型完全一致
        ...