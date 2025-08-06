# MongoDB Atlas MCP Server

这是一个基于FastMCP的MongoDB Atlas MCP服务器，用于连接和操作MongoDB Atlas数据库。

## 功能特性

- 连接MongoDB Atlas集群
- 数据库和集合管理
- 文档查询和操作
- 聚合管道支持
- 索引管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

创建 `.env` 文件并配置MongoDB Atlas连接信息：

```
MONGODB_URI=your_mongodb_atlas_connection_string
```

## 使用方法

```bash
python -m mongo_atlas_mcp.server
```

## 支持的操作

- `list_databases`: 列出所有数据库
- `list_collections`: 列出指定数据库的所有集合
- `find_documents`: 查询文档
- `insert_document`: 插入文档
- `update_document`: 更新文档
- `delete_document`: 删除文档
- `aggregate`: 执行聚合管道
- `create_index`: 创建索引
- `list_indexes`: 列出索引 