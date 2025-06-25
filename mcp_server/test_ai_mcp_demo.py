import subprocess
import sys
import os
import unittest

class TestAIMCPDemo(unittest.TestCase):
    def test_run_ai_mcp_demo(self):
        # 调用 ai-mcp-demo.py 并捕获输出
        result = subprocess.run(
            [sys.executable, 'ai-mcp-demo.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.abspath`(__file__)),
            timeout=5
        )
        # 检查进程是否正常退出
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr.decode()}")
        # 可以根据实际输出内容进一步断言
        # self.assertIn('期望的输出', result.stdout.decode())

if __name__ == "__main__":
    unittest.main()
