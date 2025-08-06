# MongoDB Atlas MCP 功能列表

本文档详细列出了MongoDB Atlas MCP服务器提供的所有功能。

## 数据库管理功能

### 1. list_databases
**功能**: 列出MongoDB Atlas中的所有数据库

**参数**: 无

**返回**: 
- `success`: 操作是否成功
- `data`: 数据库列表，包含数据库名称、大小等信息
- `count`: 数据库数量

**示例**:
```json
{
  "success": true,
  "data": [
    {
      "name": "admin",
      "size_on_disk": 1024,
      "empty": false
    },
    {
      "name": "test",
      "size_on_disk": 2048,
      "empty": false
    }
  ],
  "count": 2
}
```

### 2. list_collections
**功能**: 列出指定数据库中的所有集合

**参数**:
- `database` (string, 必需): 数据库名称

**返回**:
- `success`: 操作是否成功
- `data`: 集合列表，包含集合名称、文档数量等信息
- `count`: 集合数量

**示例**:
```json
{
  "database": "test",
  "success": true,
  "data": [
    {
      "name": "users",
      "count": 100,
      "size": 10240,
      "avg_obj_size": 102
    },
    {
      "name": "orders",
      "count": 50,
      "size": 5120,
      "avg_obj_size": 102
    }
  ],
  "count": 2
}
```

## 文档操作功能

### 3. find_documents
**功能**: 查询文档

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称
- `filter` (object, 可选): 查询过滤器
- `projection` (object, 可选): 投影字段
- `sort` (array, 可选): 排序规则
- `limit` (integer, 可选): 限制返回数量
- `skip` (integer, 可选): 跳过文档数量

**返回**:
- `success`: 操作是否成功
- `data`: 查询结果文档列表
- `count`: 返回文档数量

**示例**:
```json
{
  "database": "test",
  "collection": "users",
  "filter": {"age": {"$gte": 18}},
  "projection": {"name": 1, "email": 1},
  "sort": [("name", 1)],
  "limit": 10,
  "skip": 0
}
```

### 4. insert_document
**功能**: 插入文档

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称
- `document` (object, 必需): 要插入的文档

**返回**:
- `success`: 操作是否成功
- `data`: 包含插入文档的ID
- `count`: 插入文档数量

**示例**:
```json
{
  "database": "test",
  "collection": "users",
  "document": {
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 5. update_document
**功能**: 更新文档

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称
- `filter` (object, 必需): 更新过滤器
- `update` (object, 必需): 更新操作
- `upsert` (boolean, 可选): 是否插入不存在文档，默认false
- `multi` (boolean, 可选): 是否更新多个文档，默认false

**返回**:
- `success`: 操作是否成功
- `data`: 包含匹配数量、修改数量等信息
- `count`: 修改文档数量

**示例**:
```json
{
  "database": "test",
  "collection": "users",
  "filter": {"email": "zhangsan@example.com"},
  "update": {"$set": {"age": 26}},
  "upsert": false,
  "multi": false
}
```

### 6. delete_document
**功能**: 删除文档

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称
- `filter` (object, 必需): 删除过滤器
- `multi` (boolean, 可选): 是否删除多个文档，默认false

**返回**:
- `success`: 操作是否成功
- `data`: 包含删除文档数量
- `count`: 删除文档数量

**示例**:
```json
{
  "database": "test",
  "collection": "users",
  "filter": {"email": "zhangsan@example.com"},
  "multi": false
}
```

## 聚合操作功能

### 7. aggregate
**功能**: 执行聚合管道

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称
- `pipeline` (array, 必需): 聚合管道

**返回**:
- `success`: 操作是否成功
- `data`: 聚合结果
- `count`: 结果文档数量

**示例**:
```json
{
  "database": "test",
  "collection": "orders",
  "pipeline": [
    {"$match": {"status": "completed"}},
    {"$group": {"_id": "$user_id", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}}
  ]
}
```

## 索引管理功能

### 8. create_index
**功能**: 创建索引

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称
- `keys` (array, 必需): 索引键
- `name` (string, 可选): 索引名称
- `unique` (boolean, 可选): 是否唯一索引，默认false
- `sparse` (boolean, 可选): 是否稀疏索引，默认false
- `background` (boolean, 可选): 是否后台创建，默认true

**返回**:
- `success`: 操作是否成功
- `data`: 包含创建的索引名称
- `count`: 创建索引数量

**示例**:
```json
{
  "database": "test",
  "collection": "users",
  "keys": [["email", 1]],
  "name": "email_index",
  "unique": true,
  "sparse": false,
  "background": true
}
```

### 9. list_indexes
**功能**: 列出集合的所有索引

**参数**:
- `database` (string, 必需): 数据库名称
- `collection` (string, 必需): 集合名称

**返回**:
- `success`: 操作是否成功
- `data`: 索引列表，包含索引名称、键、属性等信息
- `count`: 索引数量

**示例**:
```json
{
  "database": "test",
  "collection": "users",
  "success": true,
  "data": [
    {
      "name": "_id_",
      "key": [["_id", 1]],
      "unique": false,
      "sparse": false,
      "background": true
    },
    {
      "name": "email_index",
      "key": [["email", 1]],
      "unique": true,
      "sparse": false,
      "background": true
    }
  ],
  "count": 2
}
```

## 错误处理

所有操作都遵循统一的错误处理格式：

**成功响应**:
```json
{
  "success": true,
  "data": {...},
  "count": 1
}
```

**错误响应**:
```json
{
  "success": false,
  "error": "错误描述信息"
}
```

## 使用注意事项

1. **连接配置**: 确保在`.env`文件中正确配置了`MONGODB_URI`
2. **权限要求**: 确保MongoDB Atlas用户具有相应的读写权限
3. **网络连接**: 确保能够访问MongoDB Atlas集群
4. **数据安全**: 在生产环境中使用前，请确保数据安全措施到位
5. **性能考虑**: 对于大量数据的操作，建议使用适当的过滤条件和限制

## 最佳实践

1. **查询优化**: 使用适当的索引来提高查询性能
2. **批量操作**: 对于大量数据操作，考虑使用批量插入/更新
3. **错误处理**: 始终检查返回的`success`字段
4. **连接管理**: 服务器会自动管理数据库连接
5. **日志记录**: 所有操作都会记录详细的日志信息 