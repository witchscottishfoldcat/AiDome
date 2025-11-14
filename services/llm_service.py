# services/llm_service.py

import logging
from abc import ABC, abstractmethod

# --- 1. 导入依赖 ---
import dashscope
from dashscope import Generation

from config.settings import settings

logger = logging.getLogger("ArkHeart.Services.LLM")

# --- 2. 定义接口 (保持不变) ---
class ILLMService(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass

# --- 3. 实现模拟服务 (保持不变) ---
class MockLLMService(ILLMService):
    def __init__(self):
        logger.info("MockLLMService initialized.")

    async def generate_response(self, prompt: str) -> str:
        logger.info(f"MockLLMService received prompt:\n---PROMPT START---\n{prompt}\n---PROMPT END---")
        mocked_response = "【模拟LLM回应】我收到了你的指令。"
        logger.info(f"MockLLMService is returning: '{mocked_response}'")
        return mocked_response

# --- 4. 实现DashScope服务 ---
class DashScopeLLMService(ILLMService):
    """使用阿里云DashScope (通义千问) API的真实LLM服务。"""
    def __init__(self):
        if not settings.DASHSCOPE_API_KEY:
            raise ValueError("DashScope API Key is not configured.")
        
        # DashScope SDK会自动从环境变量或配置中读取API Key
        dashscope.api_key = settings.DASHSCOPE_API_KEY
        self.model = settings.DASHSCOPE_MODEL
        logger.info(f"DashScopeLLMService initialized with model: {self.model}")

    async def generate_response(self, prompt: str) -> str:
        logger.info(f"Sending prompt to DashScope model '{self.model}'...")
        try:
            # DashScope SDK本身不是异步的，我们需要在异步函数中以同步方式调用
            # FastAPI会在后台线程池中运行它，不会阻塞主事件循环
            response = Generation.call(
                model=self.model,
                prompt=prompt
            )

            if response.status_code == 200:
                content = response.output.text
                logger.info(f"Received response from DashScope: '{content}'")
                return content.strip()
            else:
                error_msg = f"DashScope API error: Code {response.code}, Message: {response.message}"
                logger.error(error_msg)
                return f"抱歉，我的大脑好像短路了... ({response.code})"

        except Exception as e:
            logger.error(f"An error occurred while calling DashScope API: {e}", exc_info=True)
            return "抱歉，我的大脑好像短-路了，暂时无法思考..."

# --- 5. 实现OpenAI服务 (保持不变，以备将来使用) ---
# ... (此处省略OpenAILLMService的代码，您可以从之前版本复制过来，或者暂时删除) ...
# 为了简洁，我们暂时省略它。

# --- 6. 更新服务工厂 ---
def get_llm_service() -> ILLMService:
    """根据配置文件动态选择并返回一个LLM服务实例。"""
    provider = settings.LLM_PROVIDER
    
    if provider == 'dashscope':
        logger.info("LLM_PROVIDER is 'dashscope', loading DashScopeLLMService.")
        return DashScopeLLMService()
    
    # if provider == 'openai':
    #     ...
    
    logger.info("LLM_PROVIDER is 'mock', loading MockLLMService.")
    return MockLLMService()

# --- 7. 导出单例实例 (保持不变) ---
llm_service: ILLMService = get_llm_service()