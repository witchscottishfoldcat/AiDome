# in services/service_provider.py

from .openai_llm_service import OpenAILLMService
from .anthropic_llm_service import AnthropicLLMService # <--- 导入新类

def get_llm_service() -> ILLMService:
    if config.services.llm.provider == "OpenAI":
        return OpenAILLMService()
    elif config.services.llm.provider == "Anthropic": # <--- 添加新的逻辑分支
        return AnthropicLLMService()
    else:
        raise UnknownServiceProviderError()