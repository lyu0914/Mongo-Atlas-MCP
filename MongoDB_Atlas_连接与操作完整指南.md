# MongoDB Atlas 连接与操作完整指南

## 📋 目录
- [项目概述](#项目概述)
- [环境配置](#环境配置)
- [核心类解析](#核心类解析)
- [数据库操作](#数据库操作)
- [测试示例](#测试示例)
- [最佳实践](#最佳实践)

## 🎯 项目概述

本文介绍一个基于 Python 的 MongoDB Atlas 连接管理器，提供完整的数据库操作功能，包括连接管理、CRUD 操作、索引管理和聚合查询。

### 主要特性
- ✅ 自动连接管理
- ✅ 完整的 CRUD 操作
- ✅ 索引创建和管理
- ✅ 聚合管道支持
- ✅ 错误处理和日志记录
- ✅ 类型安全的响应对象

## 🔧 环境配置

### 1. 安装依赖
```bash
pip install pymongo dnspython python-dotenv pydantic
```

### 2. 环境变量配置
创建 `.env` 文件：
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
LOG_LEVEL=INFO
```

### 3. 项目结构
```
mongo_atlas_mcp/
├── __init__.py
├── database.py      # 核心数据库管理器
├── models.py        # 数据模型定义
└── server.py        # MCP 服务器
```

## 🏗️ 核心类解析

### MongoAtlasManager 类

这是整个系统的核心类，负责 MongoDB Atlas 的连接管理和所有数据库操作。

#### 初始化与连接
```python
class MongoAtlasManager:
    def __init__(self):
        """初始化MongoDB Atlas管理器"""
        self.client: Optional[MongoClient] = None
        self._connect()
    
    def _connect(self) -> None:
        """连接到MongoDB Atlas"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI')
            if not mongodb_uri:
                raise ValueError("MONGODB_URI环境变量未设置")
            
            self.client = MongoClient(mongodb_uri)
            # 测试连接
            self.client.admin.command('ping')
            logger.info("成功连接到MongoDB Atlas")
            
        except Exception as e:
            logger.error(f"连接MongoDB Atlas失败: {str(e)}")
            raise
```

#### 连接管理方法
```python
def get_database(self, database_name: str) -> Database:
    """获取数据库对象"""
    if not self.client:
        raise ConnectionError("MongoDB客户端未连接")
    return self.client[database_name]

def get_collection(self, database_name: str, collection_name: str) -> Collection:
    """获取集合对象"""
    database = self.get_database(database_name)
    return database[collection_name]
```

## 📊 数据库操作

### 1. 数据库管理

#### 列出所有数据库
```python
def list_databases(self) -> MongoResponse:
    """列出所有数据库"""
    try:
        databases = []
        for db_name in self.client.list_database_names():
            database_info = DatabaseInfo(
                name=db_name,
                size_on_disk=0,  # 避免权限问题
                empty=False
            )
            databases.append(database_info.model_dump())
        
        return MongoResponse(
            success=True,
            data=databases,
            count=len(databases),
            message="成功列出数据库"
        )
    except Exception as e:
        logger.error(f"列出数据库失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=str(e),
            message="列出数据库失败"
        )
```

#### 列出集合
```python
def list_collections(self, database_name: str) -> MongoResponse:
    """列出指定数据库的所有集合"""
    try:
        database = self.get_database(database_name)
        collections = []
        
        for collection_name in database.list_collection_names():
            collection_info = CollectionInfo(
                name=collection_name,
                count=0,  # 避免权限问题
                size=0,
                avg_obj_size=0
            )
            collections.append(collection_info.model_dump())
        
        return MongoResponse(
            success=True,
            data=collections,
            count=len(collections),
            message="成功列出集合"
        )
    except Exception as e:
        logger.error(f"列出集合失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=str(e),
            message="列出集合失败"
        )
```

### 2. 文档操作

#### 查询文档
```python
def find_documents(self, database_name: str, collection_name: str, 
                  filter_dict: Dict[str, Any] = None, 
                  projection: Dict[str, Any] = None,
                  sort: List[tuple] = None,
                  limit: int = None,
                  skip: int = 0) -> MongoResponse:
    """查询文档"""
    try:
        collection = self.get_collection(database_name, collection_name)
        
        cursor = collection.find(
            filter=filter_dict or {},
            projection=projection
        )
        
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        
        documents = list(cursor)
        
        # 序列化文档，将 ObjectId 转换为字符串
        serialized_documents = []
        for doc in documents:
            serialized_doc = {}
            for key, value in doc.items():
                if key == '_id':
                    serialized_doc[key] = str(value)
                else:
                    serialized_doc[key] = value
            serialized_documents.append(serialized_doc)
        
        return MongoResponse(
            success=True,
            data=serialized_documents,
            count=len(serialized_documents)
        )
    except PyMongoError as e:
        logger.error(f"查询文档失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"查询文档失败: {str(e)}"
        )
```

#### 插入文档
```python
def insert_document(self, database_name: str, collection_name: str, 
                   document: Dict[str, Any]) -> MongoResponse:
    """插入文档"""
    try:
        collection = self.get_collection(database_name, collection_name)
        result = collection.insert_one(document)
        
        return MongoResponse(
            success=True,
            data={"inserted_id": str(result.inserted_id)},
            count=1
        )
    except PyMongoError as e:
        logger.error(f"插入文档失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"插入文档失败: {str(e)}"
        )
```

#### 更新文档
```python
def update_document(self, database_name: str, collection_name: str,
                   filter_dict: Dict[str, Any], update_dict: Dict[str, Any],
                   upsert: bool = False, multi: bool = False) -> MongoResponse:
    """更新文档"""
    try:
        collection = self.get_collection(database_name, collection_name)
        
        if multi:
            result = collection.update_many(
                filter_dict, update_dict, upsert=upsert
            )
        else:
            result = collection.update_one(
                filter_dict, update_dict, upsert=upsert
            )
        
        return MongoResponse(
            success=True,
            data={
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None
            },
            count=result.modified_count
        )
    except PyMongoError as e:
        logger.error(f"更新文档失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"更新文档失败: {str(e)}"
        )
```

#### 删除文档
```python
def delete_document(self, database_name: str, collection_name: str,
                   filter_dict: Dict[str, Any], multi: bool = False) -> MongoResponse:
    """删除文档"""
    try:
        collection = self.get_collection(database_name, collection_name)
        
        if multi:
            result = collection.delete_many(filter_dict)
        else:
            result = collection.delete_one(filter_dict)
        
        return MongoResponse(
            success=True,
            data={"deleted_count": result.deleted_count},
            count=result.deleted_count
        )
    except PyMongoError as e:
        logger.error(f"删除文档失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"删除文档失败: {str(e)}"
        )
```

### 3. 聚合操作

#### 执行聚合管道
```python
def aggregate(self, database_name: str, collection_name: str,
              pipeline: List[Dict[str, Any]]) -> MongoResponse:
    """执行聚合管道"""
    try:
        collection = self.get_collection(database_name, collection_name)
        cursor = collection.aggregate(pipeline)
        results = list(cursor)
        
        return MongoResponse(
            success=True,
            data=results,
            count=len(results)
        )
    except PyMongoError as e:
        logger.error(f"执行聚合管道失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"执行聚合管道失败: {str(e)}"
        )
```

### 4. 索引管理

#### 创建索引
```python
def create_index(self, database_name: str, collection_name: str,
                 keys: List[tuple], name: str = None,
                 unique: bool = False, sparse: bool = False,
                 background: bool = True) -> MongoResponse:
    """创建索引"""
    try:
        collection = self.get_collection(database_name, collection_name)
        
        index_options = {
            "unique": unique,
            "sparse": sparse,
            "background": background
        }
        
        if name:
            index_options["name"] = name
        
        result = collection.create_index(keys, **index_options)
        
        return MongoResponse(
            success=True,
            data={"index_name": result},
            count=1
        )
    except PyMongoError as e:
        logger.error(f"创建索引失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"创建索引失败: {str(e)}"
        )
```

#### 列出索引
```python
def list_indexes(self, database_name: str, collection_name: str) -> MongoResponse:
    """列出集合的所有索引"""
    try:
        collection = self.get_collection(database_name, collection_name)
        indexes = []
        
        for index_info in collection.list_indexes():
            index_data = IndexInfo(
                name=index_info["name"],
                key=list(index_info["key"]),
                unique=index_info.get("unique", False),
                sparse=index_info.get("sparse", False),
                background=index_info.get("background", True)
            )
            indexes.append(index_data.model_dump())
        
        return MongoResponse(
            success=True,
            data=indexes,
            count=len(indexes)
        )
    except PyMongoError as e:
        logger.error(f"列出索引失败: {str(e)}")
        return MongoResponse(
            success=False,
            error=f"列出索引失败: {str(e)}"
        )
```

## 🧪 测试示例

### 1. 基本连接测试
```python
from mongo_atlas_mcp.database import MongoAtlasManager

# 创建管理器实例
manager = MongoAtlasManager()

# 测试连接
print("✅ 连接成功")
```

### 2. 数据库操作测试
```python
# 列出所有数据库
result = manager.list_databases()
print(f"数据库列表: {result.data}")

# 列出指定数据库的集合
result = manager.list_collections("test_db")
print(f"集合列表: {result.data}")
```

### 3. 文档操作测试
```python
# 插入文档
document = {
    "name": "张三",
    "age": 28,
    "email": "zhangsan@example.com",
    "city": "北京",
    "hobbies": ["读书", "游泳", "编程"],
    "created_at": "2024-01-15T10:30:00Z",
    "is_active": True,
    "score": 95.5
}

result = manager.insert_document("test_db", "users", document)
print(f"插入结果: {result.data}")

# 查询文档
result = manager.find_documents("test_db", "users")
print(f"查询结果: {result.data}")

# 更新文档
filter_dict = {"name": "张三"}
update_dict = {"$set": {"age": 29, "score": 96.0}}
result = manager.update_document("test_db", "users", filter_dict, update_dict)
print(f"更新结果: {result.data}")

# 删除文档
result = manager.delete_document("test_db", "users", {"name": "张三"})
print(f"删除结果: {result.data}")
```

### 4. 聚合操作测试
```python
# 聚合管道示例
pipeline = [
    {"$match": {"age": {"$gte": 25}}},
    {"$group": {"_id": "$city", "count": {"$sum": 1}, "avg_age": {"$avg": "$age"}}},
    {"$sort": {"count": -1}}
]

result = manager.aggregate("test_db", "users", pipeline)
print(f"聚合结果: {result.data}")
```

### 5. 索引操作测试
```python
# 创建索引
keys = [("email", 1)]
result = manager.create_index("test_db", "users", keys, name="email_index", unique=True)
print(f"创建索引结果: {result.data}")

# 列出索引
result = manager.list_indexes("test_db", "users")
print(f"索引列表: {result.data}")
```

## 📊 测试输出示例

### 数据库列表输出
```json
{
  "success": true,
  "data": [
    {
      "name": "sample_mflix",
      "size_on_disk": 0,
      "empty": false
    },
    {
      "name": "test_db",
      "size_on_disk": 0,
      "empty": false
    },
    {
      "name": "admin",
      "size_on_disk": 0,
      "empty": false
    },
    {
      "name": "local",
      "size_on_disk": 0,
      "empty": false
    }
  ],
  "count": 4,
  "message": "成功列出数据库"
}
```

### 集合列表输出
```json
{
  "success": true,
  "data": [
    {
      "name": "users",
      "count": 0,
      "size": 0,
      "avg_obj_size": 0
    },
    {
      "name": "products",
      "count": 0,
      "size": 0,
      "avg_obj_size": 0
    }
  ],
  "count": 2,
  "message": "成功列出集合"
}
```

### 插入文档输出
```json
{
  "success": true,
  "data": {
    "inserted_id": "6891e7622b3504a53dbe9e71"
  },
  "count": 1
}
```

### 查询文档输出
```json
{
  "success": true,
  "data": [
    {
      "_id": "6891e7622b3504a53dbe9e71",
      "name": "张三",
      "age": 28,
      "email": "zhangsan@example.com",
      "city": "北京",
      "hobbies": ["读书", "游泳", "编程"],
      "created_at": "2024-01-15T10:30:00Z",
      "is_active": true,
      "score": 95.5
    }
  ],
  "count": 1
}
```

## 🎯 最佳实践

### 1. 连接管理
- 使用环境变量管理连接字符串
- 实现连接池管理
- 添加连接重试机制

### 2. 错误处理
- 使用 try-catch 包装所有数据库操作
- 记录详细的错误日志
- 返回统一的错误响应格式

### 3. 性能优化
- 使用索引提升查询性能
- 合理使用投影减少数据传输
- 实现分页查询避免内存溢出

### 4. 安全性
- 使用环境变量存储敏感信息
- 实现用户权限验证
- 防止 SQL 注入（MongoDB 天然支持）

### 5. 可维护性
- 使用类型注解提高代码可读性
- 实现统一的响应格式
- 添加详细的文档注释

## 📝 总结

这个 MongoDB Atlas 连接管理器提供了完整的数据库操作功能，包括：

- ✅ 自动连接管理
- ✅ 完整的 CRUD 操作
- ✅ 聚合查询支持
- ✅ 索引管理功能
- ✅ 统一的错误处理
- ✅ 类型安全的响应

通过合理的设计和实现，可以轻松地在 Python 项目中集成 MongoDB Atlas，实现高效的数据存储和查询功能。

---

**作者**: MongoDB Atlas 连接管理器开发团队  
**版本**: 1.0.0  
**更新时间**: 2024年1月15日 