import sys
import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_nvidia_ai_endpoints import ChatNVIDIA

import warnings
warnings.filterwarnings("ignore")

load_dotenv()

async def main():
    print("1. Connecting to MCP servers and loading tools...", flush=True)
    client = MultiServerMCPClient(
        {
            "math": {
                "command": sys.executable,
                "args": ["mcp/mathserver.py"],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable-http"
            }
        }
    )

    tools = await client.get_tools()
    print(f"2. Connected! Loaded {len(tools)} tools: {[t.name for t in tools]}", flush=True)

    model = ChatNVIDIA(
        base_url="https://integrate.api.nvidia.com/v1",
        model="nvidia/nemotron-3.5-super-vl-120b-a12b",
        api_key=os.getenv("NVIDIA_API_KEY"),
        temperature=0.2,
        max_completion_tokens=2048,
    )
    agent = create_react_agent(model, tools)

    prompt = "what's (3+5) * 12 ?"
    print(f"3. Asking agent: '{prompt}' (executing multi-step tool calls, please wait ~20-30s)...", flush=True)
    math_response = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
    print("\nAgent Answer:", flush=True)
    print(math_response["messages"][-1].content, flush=True)

    prompt = "what's the weather in New York ?"
    print(f"3. Asking agent: '{prompt}' (executing multi-step tool calls, please wait ~20-30s)...", flush=True)
    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
    print("\nAgent Answer:", flush=True)
    print(weather_response["messages"][-1].content, flush=True)

asyncio.run(main())

