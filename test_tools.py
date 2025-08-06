"""
测试 MCP 工具注册
"""

import asyncio
from mongo_atlas_mcp.server import MongoAtlasMCPServer


async def test_tools():
    """测试工具注册"""
    server = MongoAtlasMCPServer()
    
    # 测试数据库连接
    print("测试数据库连接...")
    result = server.mongo_manager.list_databases()
    if result.success:
        print(f"✓ 数据库连接成功，找到 {result.count} 个数据库:")
        for db in result.data:
            print(f"  - {db['name']}")
    else:
        print(f"✗ 数据库连接失败: {result.error}")
    
    # 测试工具函数
    print("\n测试工具函数...")
    
    # 测试 list_databases 工具
    try:
        db_result = server.mongo_manager.list_databases()
        print("✓ list_databases 工具工作正常")
    except Exception as e:
        print(f"✗ list_databases 工具失败: {e}")
    
    # 测试 list_collections 工具
    try:
        coll_result = server.mongo_manager.list_collections("local")
        print("✓ list_collections 工具工作正常")
    except Exception as e:
        print(f"✗ list_collections 工具失败: {e}")
    
    server.mongo_manager.close()
    print("\n测试完成！")


if __name__ == "__main__":
    asyncio.run(test_tools()) 