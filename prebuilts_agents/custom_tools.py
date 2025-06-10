


from langchain.tools import tool

@tool("search_weather")
def get_weather(city: str) -> str:
    """根据城市名称查询天气"""
    return f"{city}天气晴朗"

get_weather
# 调用测试
print(get_weather.run("北京"))  # 输出: "北京天气晴朗"