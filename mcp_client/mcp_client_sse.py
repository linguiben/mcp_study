# 编写一个mcp client，使用sse协议与mcp server通信
import requests
import json
import time
from sseclient import SSEClient
# MCP client using SSE to communicate with the MCP server
host_info = tools.get_host_info()
host_info = json.loads(host_info)
print("[MCP Client] Host Info:", host_info)
# MCP server URL
mcp_server_url = "http://localhost:8000/sse"  # Adjust the URL as needed
def main():
    # Create a request to the MCP server to get the host info
    request_data = {
        "method": "tools.get_host_info",
        "id": 1,
        "params": {}
    }
    
    # Send the request using SSE
    response = requests.post(mcp_server_url, json=request_data)
    
    if response.status_code == 200:
        print("[MCP Client] Request sent successfully.")
    else:
        print(f"[MCP Client] Failed to send request: {response.status_code} {response.text}")
        return
    
    # Listen for SSE events
    client = SSEClient(mcp_server_url)
    
    for event in client.events():
        if event.event == 'message':
            data = json.loads(event.data)
            print("[MCP Client] Received:", data)
            if data.get("id") == 1:  # Check if this is the response we are waiting for
                break
        elif event.event == 'error':
            print("[MCP Client] Error:", event.data)
            break
        time.sleep(1)
    print("[MCP Client] Finished listening for events.")

if __name__ == "__main__":
    main()

