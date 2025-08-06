# MongoDB Atlas MCP 快速开始指南

本指南将帮助您快速设置和运行MongoDB Atlas MCP服务器。

## 前置要求

- Python 3.10 或更高版本
- MongoDB Atlas 账户和集群
- 网络连接到MongoDB Atlas

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone https://github.com/lyu0914/Mongo-Atlas-MCP.git
cd mongo-atlas-mcp
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或者使用开发模式安装：

```bash
pip install -e .
```

### 3. 配置环境变量

复制环境变量示例文件：

```bash
cp env.example .env
```

编辑 `.env` 文件，设置您的MongoDB Atlas连接字符串：

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
```

**注意**: 请将上述连接字符串替换为您的实际MongoDB Atlas连接字符串。

### 4. 测试连接

运行测试脚本来验证连接：

```bash
python test_mongo_atlas_mcp.py
```

如果所有测试都通过，说明配置正确。

### 5. 启动MCP服务器

```bash
python run_server.py
```

或者使用模块方式启动：

```bash
python -m mongo_atlas_mcp.server
```

## 使用示例

### 基本操作示例

1. **列出所有数据库**
```python
# 通过MCP客户端调用
result = await client.call_tool("list_databases", {})
```

2. **列出指定数据库的集合**
```python
result = await client.call_tool("list_collections", {
    "database": "test"
})
```

3. **插入文档**
```python
result = await client.call_tool("insert_document", {
    "database": "test",
    "collection": "users",
    "document": {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    }
})
```

4. **查询文档**
```python
result = await client.call_tool("find_documents", {
    "database": "test",
    "collection": "users",
    "filter": {"age": {"$gte": 18}},
    "limit": 10
})
```

5. **更新文档**
```python
result = await client.call_tool("update_document", {
    "database": "test",
    "collection": "users",
    "filter": {"email": "zhangsan@example.com"},
    "update": {"$set": {"age": 26}}
})
```

6. **删除文档**
```python
result = await client.call_tool("delete_document", {
    "database": "test",
    "collection": "users",
    "filter": {"email": "zhangsan@example.com"}
})
```

7. **执行聚合管道**
```python
result = await client.call_tool("aggregate", {
    "database": "test",
    "collection": "orders",
    "pipeline": [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": "$user_id", "total": {"$sum": "$amount"}}}
    ]
})
```

8. **创建索引**
```python
result = await client.call_tool("create_index", {
    "database": "test",
    "collection": "users",
    "keys": [["email", 1]],
    "name": "email_index",
    "unique": True
})
```

## 故障排除

### 常见问题

1. **连接失败**
   - 检查MONGODB_URI是否正确
   - 确认网络连接正常
   - 验证MongoDB Atlas用户权限

2. **权限错误**
   - 确保MongoDB Atlas用户具有读写权限
   - 检查IP白名单设置

3. **依赖安装失败**
   - 确保Python版本为3.10+
   - 尝试升级pip: `pip install --upgrade pip`

4. **测试失败**
   - 检查.env文件配置
   - 确认MongoDB Atlas集群状态

### 日志查看

服务器运行时会输出详细的日志信息，包括：
- 连接状态
- 操作结果
- 错误信息

## 生产环境部署

1. **安全配置**
   - 使用强密码
   - 启用IP白名单
   - 配置SSL连接

2. **性能优化**
   - 创建适当的索引
   - 使用连接池
   - 监控查询性能

3. **监控和日志**
   - 配置日志轮转
   - 设置监控告警
   - 定期备份数据

## 支持

如果遇到问题，请：

1. 查看日志输出
2. 运行测试脚本验证配置
3. 检查MongoDB Atlas文档
4. 提交Issue到GitHub仓库

## 许可证


本项目采用MIT许可证，详见LICENSE文件。 
