"""
验证插入的文档
"""

from mongo_atlas_mcp.database import MongoAtlasManager
from dotenv import load_dotenv

def verify_inserted_document():
    """验证插入的文档"""
    # 加载环境变量
    load_dotenv()
    
    # 创建数据库管理器
    manager = MongoAtlasManager()
    
    try:
        # 查询刚才插入的文档
        print("正在查询插入的文档...")
        result = manager.find_documents(
            database_name="test_mcp_db",
            collection_name="test_collection",
            filter_dict={"name": "测试文档"}
        )
        
        if result.success:
            print("✓ 查询成功！")
            print(f"找到 {result.count} 个文档:")
            
            for i, doc in enumerate(result.data, 1):
                print(f"\n文档 {i}:")
                print(f"  ID: {doc.get('_id')}")
                print(f"  名称: {doc.get('name')}")
                print(f"  描述: {doc.get('description')}")
                print(f"  时间戳: {doc.get('timestamp')}")
                print(f"  标签: {doc.get('tags')}")
                print(f"  作者: {doc.get('author')}")
                print(f"  版本: {doc.get('version')}")
                if 'metadata' in doc:
                    print(f"  元数据: {doc['metadata']}")
        else:
            print("✗ 查询失败！")
            print(f"错误: {result.error}")
            
    except Exception as e:
        print(f"✗ 查询文档时发生异常: {str(e)}")
    
    finally:
        # 关闭连接
        manager.close()
        print("\n数据库连接已关闭")

if __name__ == "__main__":
    verify_inserted_document() 