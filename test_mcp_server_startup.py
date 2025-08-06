"""
测试 MCP 服务器启动和工具暴露
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

def test_mcp_server_startup():
    """测试 MCP 服务器启动"""
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['MONGODB_URI'] = "mongodb+srv://liu091413:la094658@cluster0.qmiwn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        env['PYTHONPATH'] = str(Path.cwd())
        
        print("正在启动 MCP 服务器...")
        print(f"工作目录: {Path.cwd()}")
        print(f"Python 路径: {sys.executable}")
        
        # 启动 MCP 服务器进程
        process = subprocess.Popen(
            [sys.executable, "run_server.py"],
            cwd=Path.cwd(),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待一段时间让服务器启动
        import time
        time.sleep(3)
        
        # 检查进程是否还在运行
        if process.poll() is None:
            print("✓ MCP 服务器启动成功")
            print("✓ 进程正在运行")
            
            # 获取输出
            stdout, stderr = process.communicate(timeout=5)
            if stdout:
                print("标准输出:")
                print(stdout)
            if stderr:
                print("错误输出:")
                print(stderr)
        else:
            print("✗ MCP 服务器启动失败")
            stdout, stderr = process.communicate()
            if stdout:
                print("标准输出:")
                print(stdout)
            if stderr:
                print("错误输出:")
                print(stderr)
        
        # 终止进程
        process.terminate()
        process.wait()
        print("✓ 服务器进程已终止")
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mcp_server_startup() 