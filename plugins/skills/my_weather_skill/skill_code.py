# in plugins/skills/my_weather_skill/skill_code.py

import requests
from ..base import BaseSkill, SkillResult

class WeatherSkill(BaseSkill):
    # execute方法是必须的，它是技能的入口
    # args 参数是由LLM根据用户问题解析出的结构化数据
    async def execute(self, args: dict) -> SkillResult:
        city = args.get("city", "北京") # 提供一个默认值
        
        # 由于我们在plugin.json中请求了网络权限，所以这里可以安全地进行API调用
        try:
            # 注意：真实的URL应该从配置文件或环境变量中获取
            response = requests.get(f"https://api.weather.com/v1/today?city={city}")
            response.raise_for_status() # 如果请求失败则抛出异常
            
            weather_data = response.json()
            report = f"{city}今天的天气是：{weather_data['condition']}，温度 {weather_data['temperature']}摄氏度。"
            
            # 返回一个成功的SkillResult对象，其中data可以被LLM用于生成最终的自然语言回答
            return SkillResult(success=True, data={"report": report})

        except requests.RequestException as e:
            # 如果发生任何网络错误，返回一个失败的SkillResult，并附上对AI友好的错误信息
            return SkillResult(success=False, error_message=f"网络请求失败，我无法连接到天气服务。错误: {e}")