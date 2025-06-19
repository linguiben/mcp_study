# tools.py
import platform
import psutil
import subprocess
import json

def get_host_info() -> str:
    """get host information

    Returns:
        str: the host information in JSON string
    """
    info: dict[str, str] = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": str(round(psutil.virtual_memory().total / (1024**3), 2)),
    }

    cpu_count = psutil.cpu_count(logical=True)
    if cpu_count is None:
        info["cpu_count"] = "-1"
    else:
        info["cpu_count"] = str(cpu_count)
    
    try:
        cpu_model = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"]
        ).decode().strip()
        info["cpu_model"] = cpu_model
    except Exception:
        info["cpu_model"] = "Unknown"

    return json.dumps(info, indent=4)

def get_file_in_base64(file_path: str) -> str:
    """Get the content of a file in base64 encoding.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The base64 encoded content of the file.
    """
    import base64
    import os
    if(not os.path.exists(file_path)):
        print(f"File not found: {file_path}")
        return ""
    with open(file_path, "rb") as file:
        file_content = file.read()
    return base64.b64encode(file_content).decode('utf-8')

if __name__ == '__main__':
    #print(get_host_info())
    print(get_file_in_base64("./data/202506192319_google_finance.png"))

# This code can be used to get the host information in a structured format.
# It can be integrated into a larger application or used standalone.
# The output will be a JSON string containing the system information.