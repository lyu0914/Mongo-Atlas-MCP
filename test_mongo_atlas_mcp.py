"""
MongoDB Atlas MCP 服务器安全测试文件

用于测试MCP服务器的各项功能，避免权限问题
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

from mongo_atlas_mcp.database import MongoAtlasManager
from mongo_atlas_mcp.models import MongoResponse

# 添加项目路径到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))




def test_database_connection():
    """
    测试数据库连接功能
    
    验证MongoDB Atlas连接是否正常
    """
    print("=== 测试数据库连接 ===")
    try:
        manager = MongoAtlasManager()
        print("✓ MongoDB Atlas连接成功")
        
        # 测试列出数据库
        result = manager.list_databases()
        if result.success:
            print(f"✓ 成功列出 {result.count} 个数据库")
            for db in result.data:
                print(f"  - {db['name']}")
        else:
            print(f"✗ 列出数据库失败: {result.error}")
        
        manager.close()
        return True
        
    except Exception as e:
        print(f"✗ 数据库连接失败: {str(e)}")
        return False


def test_basic_operations():
    """
    测试基本操作功能
    
    验证基本的增删改查操作
    """
    print("\n=== 测试基本操作 ===")
    try:
        manager = MongoAtlasManager()
        
        # 测试数据库和集合
        test_db = "test_mcp_db"
        test_collection = "test_collection"
        
        # 插入测试文档
        test_doc = {
            "name": "测试文档",
            "value": 123,
            "tags": ["test", "mcp"],
            "timestamp": "2024-01-01"
        }
        
        print("1. 测试插入文档...")
        result = manager.insert_document(test_db, test_collection, test_doc)
        if result.success:
            print("✓ 插入文档成功")
            inserted_id = result.data["inserted_id"]
            print(f"  插入的文档ID: {inserted_id}")
        else:
            print(f"✗ 插入文档失败: {result.error}")
            return False
        
        # 查询文档
        print("2. 测试查询文档...")
        result = manager.find_documents(test_db, test_collection, {"name": "测试文档"})
        if result.success and result.count > 0:
            print("✓ 查询文档成功")
            print(f"  找到 {result.count} 个文档")
            for doc in result.data:
                print(f"  - {doc}")
        else:
            print(f"✗ 查询文档失败: {result.error}")
        
        # 更新文档
        print("3. 测试更新文档...")
        update_result = manager.update_document(
            test_db, test_collection,
            {"name": "测试文档"},
            {"$set": {"value": 456, "updated": True}}
        )
        if update_result.success:
            print("✓ 更新文档成功")
            print(f"  更新了 {update_result.data['modified_count']} 个文档")
        else:
            print(f"✗ 更新文档失败: {update_result.error}")
        
        # 验证更新结果
        print("4. 验证更新结果...")
        result = manager.find_documents(test_db, test_collection, {"name": "测试文档"})
        if result.success and result.count > 0:
            print("✓ 验证更新成功")
            for doc in result.data:
                print(f"  - 更新后的文档: {doc}")
        
        # 删除文档
        print("5. 测试删除文档...")
        delete_result = manager.delete_document(
            test_db, test_collection,
            {"name": "测试文档"}
        )
        if delete_result.success:
            print("✓ 删除文档成功")
            print(f"  删除了 {delete_result.data['deleted_count']} 个文档")
        else:
            print(f"✗ 删除文档失败: {delete_result.error}")
        
        # 验证删除结果
        print("6. 验证删除结果...")
        result = manager.find_documents(test_db, test_collection, {"name": "测试文档"})
        if result.success and result.count == 0:
            print("✓ 验证删除成功，文档已删除")
        else:
            print("✗ 验证删除失败，文档仍然存在")
        
        manager.close()
        return True
        
    except Exception as e:
        print(f"✗ 基本操作测试失败: {str(e)}")
        return False


def test_aggregation():
    """
    测试聚合操作功能
    
    验证MongoDB聚合管道操作
    """
    print("\n=== 测试聚合操作 ===")
    try:
        manager = MongoAtlasManager()
        
        test_db = "test_mcp_db"
        test_collection = "test_aggregation"
        
        # 插入测试数据
        test_docs = [
            {"name": "产品A", "category": "电子产品", "price": 100, "sales": 50},
            {"name": "产品B", "category": "电子产品", "price": 200, "sales": 30},
            {"name": "产品C", "category": "服装", "price": 80, "sales": 100},
            {"name": "产品D", "category": "服装", "price": 120, "sales": 80}
        ]
        
        print("1. 插入测试数据...")
        for doc in test_docs:
            result = manager.insert_document(test_db, test_collection, doc)
            if not result.success:
                print(f"✗ 插入测试数据失败: {result.error}")
                return False
        
        print("✓ 插入测试数据成功")
        
        # 测试聚合操作 - 按类别分组统计
        print("2. 测试聚合操作...")
        pipeline = [
            {"$group": {
                "_id": "$category",
                "total_sales": {"$sum": "$sales"},
                "avg_price": {"$avg": "$price"},
                "product_count": {"$sum": 1}
            }},
            {"$sort": {"total_sales": -1}}
        ]
        
        result = manager.aggregate(test_db, test_collection, pipeline)
        if result.success:
            print("✓ 聚合操作成功")
            print(f"  聚合结果:")
            for doc in result.data:
                print(f"  - 类别: {doc['_id']}")
                print(f"    总销量: {doc['total_sales']}")
                print(f"    平均价格: {doc['avg_price']:.2f}")
                print(f"    产品数量: {doc['product_count']}")
        else:
            print(f"✗ 聚合操作失败: {result.error}")
        
        # 清理测试数据
        print("3. 清理测试数据...")
        delete_result = manager.delete_document(test_db, test_collection, {})
        if delete_result.success:
            print("✓ 清理测试数据成功")
        else:
            print(f"✗ 清理测试数据失败: {delete_result.error}")
        
        manager.close()
        return True
        
    except Exception as e:
        print(f"✗ 聚合操作测试失败: {str(e)}")
        return False


def test_index_operations():
    """
    测试索引操作功能
    
    验证索引的创建和查询
    """
    print("\n=== 测试索引操作 ===")
    try:
        manager = MongoAtlasManager()
        
        test_db = "test_mcp_db"
        test_collection = "test_index"
        
        # 插入测试数据
        test_docs = [
            {"name": "用户A", "email": "userA@example.com", "age": 25},
            {"name": "用户B", "email": "userB@example.com", "age": 30},
            {"name": "用户C", "email": "userC@example.com", "age": 35}
        ]
        
        print("1. 插入测试数据...")
        for doc in test_docs:
            result = manager.insert_document(test_db, test_collection, doc)
            if not result.success:
                print(f"✗ 插入测试数据失败: {result.error}")
                return False
        
        print("✓ 插入测试数据成功")
        
        # 创建索引
        print("2. 创建索引...")
        index_result = manager.create_index(
            test_db, test_collection,
            keys=[("email", 1)],
            name="email_index",
            unique=True
        )
        
        if index_result.success:
            print("✓ 创建索引成功")
            print(f"  索引名称: {index_result.data['index_name']}")
        else:
            print(f"✗ 创建索引失败: {index_result.error}")
        
        # 列出索引
        print("3. 列出索引...")
        list_result = manager.list_indexes(test_db, test_collection)
        if list_result.success:
            print("✓ 列出索引成功")
            print(f"  找到 {list_result.count} 个索引:")
            for index in list_result.data:
                print(f"  - {index['name']}: {index['key']}")
        else:
            print(f"✗ 列出索引失败: {list_result.error}")
        
        # 清理测试数据
        print("4. 清理测试数据...")
        delete_result = manager.delete_document(test_db, test_collection, {})
        if delete_result.success:
            print("✓ 清理测试数据成功")
        else:
            print(f"✗ 清理测试数据失败: {delete_result.error}")
        
        manager.close()
        return True
        
    except Exception as e:
        print(f"✗ 索引操作测试失败: {str(e)}")
        return False


def main():
    """
    主测试函数
    
    运行所有测试用例
    """
    print("MongoDB Atlas MCP 服务器安全测试")
    print("=" * 50)
    
    # 检查环境变量
    load_dotenv()
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        print("错误: 未设置MONGODB_URI环境变量")
        print("请创建.env文件并设置MongoDB Atlas连接字符串")
        print("示例:")
        print("MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority")
        return
    
    print(f"使用连接字符串: {mongodb_uri[:50]}...")
    print()
    
    # 运行测试
    tests = [
        ("数据库连接", test_database_connection),
        ("基本操作", test_basic_operations),
        ("聚合操作", test_aggregation),
        ("索引操作", test_index_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} 测试通过")
            else:
                print(f"✗ {test_name} 测试失败")
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {str(e)}")
        print()
    
    print("=" * 50)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！MongoDB Atlas MCP 服务器运行正常")
    else:
        print("⚠️  部分测试失败，请检查配置和权限")


if __name__ == "__main__":
    main()