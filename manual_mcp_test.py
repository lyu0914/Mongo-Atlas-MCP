"""
手动测试 MCP 服务器
"""

import asyncio
import json
import sys
from mongo_atlas_mcp.server import MongoAtlasMCPServer

async def test_mcp_manual():
    """手动测试 MCP 服务器"""
    try:
        # 创建服务器
        server = MongoAtlasMCPServer()
        print("✓ 服务器创建成功")
        
        # 获取工具列表
        tools = await server.mcp.get_tools()
        print(f"✓ 工具数量: {len(tools)}")
        
        # 模拟 MCP 协议握手
        print("\n模拟 MCP 协议握手...")
        
        # 测试工具调用
        print("\n测试工具调用...")
        
        # 测试 list_databases
        print("测试 list_databases 工具...")
        result = server.mongo_manager.list_databases()
        if result.success:
            print(f"✓ 数据库列表获取成功，找到 {result.count} 个数据库")
            for db in result.data:
                print(f"  - {db['name']}")
        else:
            print(f"✗ 数据库列表获取失败: {result.error}")
        
        # 测试 list_collections
        print("\n测试 list_collections 工具...")
        result = server.mongo_manager.list_collections("test_mcp_db")
        if result.success:
            print(f"✓ 集合列表获取成功，找到 {result.count} 个集合")
            for coll in result.data:
                print(f"  - {coll['name']}")
        else:
            print(f"✗ 集合列表获取失败: {result.error}")
        
        # 关闭连接
        server.mongo_manager.close()
        print("\n✓ 测试完成")
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_manual()) 