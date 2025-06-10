from mcp.server import FastMCP

mcp = FastMCP("math")

@mcp.tool()
def add(a:int, b:int) -> int:
    """ 两数相加"""
    return  a + b

@mcp.tool()
def multiply(a:int , b:int) -> int:
    """两数相乘"""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")

