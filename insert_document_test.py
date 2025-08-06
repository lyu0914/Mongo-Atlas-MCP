"""
测试插入文档到 MongoDB Atlas
"""

from mongo_atlas_mcp.database import MongoAtlasManager
from dotenv import load_dotenv
import os

def test_insert_document():
    """测试插入文档"""
    # 加载环境变量
    load_dotenv()
    
    # 创建数据库管理器
    manager = MongoAtlasManager()
    
    # 准备要插入的文档
    document = {
        "name": "测试文档",
        "description": "这是一个通过MCP服务器插入的测试文档",
        "timestamp": "2024-01-15",
        "tags": ["mcp", "test", "mongodb"],
        "author": "MCP用户",
        "version": "1.0.0",
        "metadata": {
            "created_by": "mongo_atlas_mcp",
            "environment": "development"
        }
    }
    
    try:
        # 插入文档
        print("正在插入文档到 test_mcp_db.test_collection...")
        result = manager.insert_document(
            database_name="test_mcp_db",
            collection_name="test_collection",
            document=document
        )
        
        if result.success:
            print("✓ 文档插入成功！")
            print(f"插入的文档ID: {result.data['inserted_id']}")
            print(f"影响文档数量: {result.count}")
            print(f"消息: {result.message}")
        else:
            print("✗ 文档插入失败！")
            print(f"错误: {result.error}")
            
    except Exception as e:
        print(f"✗ 插入文档时发生异常: {str(e)}")
    
    finally:
        # 关闭连接
        manager.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    test_insert_document() 