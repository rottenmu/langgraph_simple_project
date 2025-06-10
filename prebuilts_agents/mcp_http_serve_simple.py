import mcp
from mcp.server import FastMCP

mcp = FastMCP("myMcp")


@mcp.tool()
def query_db() -> str:
    """To that use initialized  resources"""
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context["db"]
    return db.run()


@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location"""
    return "杭州今天是晴天"

@mcp.tool()
def look_up_linux():
    """检测操作系统内存"""
    return f"内存正常，cpu正常"

@mcp.resource("gretting://{name}")
def get_greeting(name:str) -> str:
    """ greeting name"""
    return f"Hello{name}"



if __name__ =="__main__":
    mcp.run(transport="streamable-http")