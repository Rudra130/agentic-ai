from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math MCP server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers
    """
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """
    Subtract two numbers
    """
    return a - b

@mcp.tool()
def mul(a: int, b: int) -> int:
    """
    Multiply two numbers
    """
    return a * b

@mcp.tool()
def div(a: int, b: int) -> int:
    """
    Divide two numbers
    """
    if b==0:
        return 0;

    return a / b            

# The transpost ="stdio" argument tell the server to:
# 1. Communicate using standard input and output
# 2. Listen for connection requests from clients
# 3. Respond to client requests
# 4. Close the connection when the client disconnects

if __name__ == "__main__":
    mcp.run(transport="stdio")

