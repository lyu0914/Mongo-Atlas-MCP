"""
测试 MCP 工具注册
"""

import asyncio
from mongo_atlas_mcp.server import MongoAtlasMCPServer

async def test_mcp_tools():
    """测试 MCP 工具注册"""
    try:
        # 创建 MCP 服务器
        server = MongoAtlasMCPServer()
        print("✓ MCP 服务器创建成功")
        
        # 检查工具数量
        tools = await server.mcp.get_tools()
        print(f"✓ 注册的工具数量: {len(tools)}")
        
        # 列出所有工具
        print("\n注册的工具:")
        for i, tool in enumerate(tools, 1):
            if isinstance(tool, str):
                print(f"  {i}. {tool}")
            else:
                print(f"  {i}. {type(tool)}: {tool}")
        
        # 测试数据库连接
        print("\n测试数据库连接...")
        result = server.mongo_manager.list_databases()
        if result.success:
            print(f"✓ 数据库连接成功，找到 {result.count} 个数据库")
        else:
            print(f"✗ 数据库连接失败: {result.error}")
        
        # 关闭连接
        server.mongo_manager.close()
        print("✓ 数据库连接已关闭")
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_tools()) 