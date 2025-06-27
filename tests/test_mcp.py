from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import subprocess
import asyncio
import os


# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["-u", "../src/dnd_mcp/server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(
                read, write, sampling_callback=handle_sampling_message
            ) as session:
                # Initialize the connection
                print("Initializing MCP session...")
                await session.initialize()
                print("✅ Session initialized successfully!")

                # List available tools (not prompts - this server has tools)
                print("\n=== Available Tools ===")
                tools = await session.list_tools()
                print(f"Found {len(tools.tools)} tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Test loading a character
                print("\n=== Testing Character Loading ===")
                char_path = "../examples/characters/gandalf.json"
                if os.path.exists(char_path):
                    result = await session.call_tool(
                        "load_character", 
                        arguments={"file_path": char_path}
                    )
                    print(f"Load result: {result.content[0].text}")
                    
                    # Get character info
                    print("\n=== Getting Character Info ===")
                    result = await session.call_tool("get_character_info", arguments={})
                    print(f"Character info: {result.content[0].text}")
                    
                    # Test a skill check
                    print("\n=== Testing Skill Check ===")
                    result = await session.call_tool(
                        "roll_skill_check", 
                        arguments={"skill": "perception", "modifiers": "advantage +2"}
                    )
                    print(f"Perception check: {result.content[0].text}")
                    
                    # Test ability check
                    print("\n=== Testing Ability Check ===")
                    result = await session.call_tool(
                        "roll_ability_check", 
                        arguments={"ability": "int", "modifiers": "guidance:1d4"}
                    )
                    print(f"Intelligence check: {result.content[0].text}")
                    
                    # List available skills
                    print("\n=== Available Skills ===")
                    result = await session.call_tool("list_available_skills", arguments={})
                    print(f"Skills: {result.content[0].text}")
                    
                else:
                    print(f"Character file not found: {char_path}")
                    print("Testing without loading a character...")
                    
                    # Try to get character info (should fail gracefully)
                    result = await session.call_tool("get_character_info", arguments={})
                    print(f"No character loaded result: {result.content[0].text}")

    except Exception as e:
        print(f"Error during MCP test: {e}")
        import traceback
        traceback.print_exc()


async def test_server_directly():
    """Test if the server script runs at all"""
    print("\n=== Testing Server Directly ===")
    try:
        result = subprocess.run(
            ["python", "../src/dnd_mcp/server.py"], 
            capture_output=True, 
            text=True, 
            timeout=3  # Shorter timeout
        )
        print(f"Server stdout: {result.stdout}")
        print(f"Server stderr: {result.stderr}")
        print(f"Return code: {result.returncode}")
    except subprocess.TimeoutExpired:
        print("✅ Server is running (didn't exit within 3 seconds - this is expected)")
    except Exception as e:
        print(f"❌ Error running server: {e}")


if __name__ == "__main__":
    print("=== D&D MCP Server Test ===")
    
    # First test if server runs
    asyncio.run(test_server_directly())
    
    # Then test MCP connection
    print("\n=== Testing MCP Connection ===")
    asyncio.run(run())