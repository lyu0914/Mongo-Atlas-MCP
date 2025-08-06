"""
查询 test_mcp_db 数据库中的所有集合
"""

from mongo_atlas_mcp.database import MongoAtlasManager
from dotenv import load_dotenv

def list_collections():
    """查询 test_mcp_db 数据库中的所有集合"""
    # 加载环境变量
    load_dotenv()
    
    # 创建数据库管理器
    manager = MongoAtlasManager()
    
    try:
        # 查询 test_mcp_db 数据库中的所有集合
        print("正在查询 test_mcp_db 数据库中的所有集合...")
        result = manager.list_collections("test_mcp_db")
        
        if result.success:
            print("✓ 查询成功！")
            print(f"找到 {result.count} 个集合:")
            
            if result.data:
                for i, collection in enumerate(result.data, 1):
                    print(f"  {i}. {collection['name']}")
                    print(f"     文档数量: {collection['count']}")
                    print(f"     集合大小: {collection['size']} 字节")
                    print(f"     平均对象大小: {collection['avg_obj_size']} 字节")
                    print()
            else:
                print("  该数据库中没有集合")
        else:
            print("✗ 查询失败！")
            print(f"错误: {result.error}")
            
    except Exception as e:
        print(f"✗ 查询集合时发生异常: {str(e)}")
    
    finally:
        # 关闭连接
        manager.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    list_collections() 