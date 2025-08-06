#!/usr/bin/env python3
"""
MongoDB Atlas MCP 服务器启动脚本

用于启动MCP服务器
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# 添加项目路径到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mongo_atlas_mcp.server import MongoAtlasMCPServer


def main():
    """
    主启动函数
    
    启动MongoDB Atlas MCP服务器
    """
    # 加载环境变量
    load_dotenv()
    
    # 检查环境变量
    if not os.getenv('MONGODB_URI'):
        print("错误: 未设置MONGODB_URI环境变量")
        print("请创建.env文件并设置MongoDB Atlas连接字符串")
        print("参考env.example文件")
        return
    
    try:
        # 创建并启动服务器
        server = MongoAtlasMCPServer()
        print("MongoDB Atlas MCP 服务器启动中...")
        print("按 Ctrl+C 停止服务器")
        
        # 运行服务器
        asyncio.run(server.run())
        
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {str(e)}")


if __name__ == "__main__":
    main() 