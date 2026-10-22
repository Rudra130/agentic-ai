from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather MCP server")

@mcp.tool()
async def get_weather(city: str) -> dict:
    """
    Get the weather for a city
    """
    return {
        "city": city,
        "temperature": "25",
        "unit": "celsius"
    }

@mcp.tool()
async def get_forecast(city: str, days: int) -> dict:
    """
    Get the forecast for a city
    """
    return {
        "city": city,
        "days": days,
        "forecast": [
            {"day": "1", "temperature": "25", "unit": "celsius"},
            {"day": "2", "temperature": "26", "unit": "celsius"},
            {"day": "3", "temperature": "27", "unit": "celsius"}
        ]
    }

# The transport ="streamable-http" argument tells the server to:
# 1. Communicate using HTTP POST requests
# 2. Listen for connection requests from clients
# 3. Respond to client requests
# 4. Close the connection when the client disconnects

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
