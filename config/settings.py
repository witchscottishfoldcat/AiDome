# config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # --- LLM Provider Settings ---
    LLM_PROVIDER: Literal['mock', 'openai', 'dashscope'] = 'mock'
    
    # --- OpenAI Specific Settings ---
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # --- Alibaba Cloud DashScope (Lingma) Settings ---
    DASHSCOPE_API_KEY: str | None = None
    DASHSCOPE_MODEL: str = "qwen-turbo" # 默认使用通义千问-turbo

settings = Settings()

# --- 启动时验证逻辑更新 ---
if settings.LLM_PROVIDER == 'openai' and not settings.OPENAI_API_KEY:
    raise ValueError("LLM_PROVIDER is set to 'openai', but OPENAI_API_KEY is not configured.")
if settings.LLM_PROVIDER == 'dashscope' and not settings.DASHSCOPE_API_KEY:
    raise ValueError("LLM_PROVIDER is 'dashscope', but DASHSCOPE_API_KEY is not configured.")