import subprocess
import json
import sys

# 启动 ai-mcp-demo.py 进程，使用 stdio 通信
proc = subprocess.Popen(
    [sys.executable, "ai-mcp-demo.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 构造一个 MCP 协议的请求，假设支持列出 tools 的方法（如 list_tools 或 openapi/schema）
# 这里以通用的 openapi.schema 为例，实际方法名请根据 FastMCP 实现调整
list_tools_request = json.dumps({
    "method": "openapi.schema",
    "id": 1,
    "params": {}
}) + "\n"

proc.stdin.write(list_tools_request)
proc.stdin.flush()

# 读取响应
response = proc.stdout.readline()
print("[MCP openapi.schema 响应]", response)

# 解析响应，查找 get_host_info 工具
schema = json.loads(response)
tool_name = None
for name in schema.get("result", {}).get("tools", {}):
    if name == "get_host_info":
        tool_name = name
        break

if not tool_name:
    print("未找到 get_host_info 工具")
    proc.terminate()
    sys.exit(1)

# 构造调用 get_host_info 的请求
call_tool_request = json.dumps({
    "method": "tools.get_host_info",
    "id": 2,
    "params": {}
}) + "\n"
proc.stdin.write(call_tool_request)
proc.stdin.flush()

# 读取响应
response2 = proc.stdout.readline()
print("[MCP get_host_info 响应]", response2)

proc.terminate()
