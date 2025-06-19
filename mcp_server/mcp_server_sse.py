# MCP = modle control protocol, invented by Anthropic
# This is a demo of how to use MCP with a custom tool
# and run it with FastMCP, a fast implementation of MCP.
# The tool will return the host information in JSON format.
# The MCP server will run and listen for requests, responding with the host information.
# The server can be run with different transports, such as stdio or SSE.
from mcp.server.fastmcp import FastMCP
import mcp_server.tools as tools

mcp = FastMCP("host info mcp") # Create a FastMCP instance with a name
mcp.add_tool(tools.get_host_info) # Add the custom tool to the MCP instance

@mcp.tool()
def foo():
    return ""

# stido transport is useful for local testing, while sse is useful for web applications.
def main():
    # mcp.run("stdio") # Run the MCP server with stdio transport or sse (Server-Sent Events)
    mcp.run("sse")  # Run the MCP server with SSE transport
    # mcp.run("streamable-http")

if __name__ == "__main__":
    main()


