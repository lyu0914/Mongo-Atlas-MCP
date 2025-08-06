"""
MongoDB Atlas MCP Server

基于FastMCP的MongoDB Atlas连接和操作服务器
遵循MCP协议和JSON-RPC 2.0协议
"""

import asyncio
import logging
from typing import Dict, Any, List
from fastmcp import FastMCP

try:
    from .database import MongoAtlasManager
except ImportError:
    from database import MongoAtlasManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoAtlasMCPServer:
    """
    MongoDB Atlas MCP 服务器
    
    提供MongoDB Atlas的连接和操作功能
    """
    
    def __init__(self):
        """初始化MCP服务器"""
        self.mongo_manager = MongoAtlasManager()
        self.mcp = FastMCP()
        self._register_tools()
    
    def _register_tools(self) -> None:
        """注册所有可用的工具"""
        
        # 使用装饰器注册工具
        @self.mcp.tool
        def list_databases() -> Dict[str, Any]:
            """列出MongoDB Atlas中的所有数据库"""
            try:
                result = self.mongo_manager.list_databases()
                return result.model_dump()
            except Exception as e:
                logger.error(f"列出数据库失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"列出数据库失败: {str(e)}"
                }
        
        @self.mcp.tool
        def list_collections(database: str) -> Dict[str, Any]:
            """列出指定数据库中的所有集合"""
            try:
                result = self.mongo_manager.list_collections(database)
                return result.model_dump()
            except Exception as e:
                logger.error(f"列出集合失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"列出集合失败: {str(e)}"
                }
        
        @self.mcp.tool
        def find_documents(
            database: str, 
            collection: str, 
            filter: Dict[str, Any] = None,
            projection: Dict[str, Any] = None,
            sort: List = None,
            limit: int = None,
            skip: int = 0
        ) -> Dict[str, Any]:
            """查询文档"""
            try:
                result = self.mongo_manager.find_documents(
                    database, collection, filter, projection, sort, limit, skip
                )
                return result.model_dump()
            except Exception as e:
                logger.error(f"查询文档失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"查询文档失败: {str(e)}"
                }
        
        @self.mcp.tool
        def insert_document(
            database: str, 
            collection: str,
            document: Dict[str, Any]
        ) -> Dict[str, Any]:
            """插入文档"""
            try:
                result = self.mongo_manager.insert_document(database, collection, document)
                return result.model_dump()
            except Exception as e:
                logger.error(f"插入文档失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"插入文档失败: {str(e)}"
                }
        
        @self.mcp.tool
        def update_document(
            database: str, 
            collection: str,
            filter: Dict[str, Any], 
            update: Dict[str, Any],
            upsert: bool = False, 
            multi: bool = False
        ) -> Dict[str, Any]:
            """更新文档"""
            try:
                result = self.mongo_manager.update_document(
                    database, collection, filter, update, upsert, multi
                )
                return result.model_dump()
            except Exception as e:
                logger.error(f"更新文档失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"更新文档失败: {str(e)}"
                }
        
        @self.mcp.tool
        def delete_document(
            database: str, 
            collection: str,
            filter: Dict[str, Any], 
            multi: bool = False
        ) -> Dict[str, Any]:
            """删除文档"""
            try:
                result = self.mongo_manager.delete_document(database, collection, filter, multi)
                return result.model_dump()
            except Exception as e:
                logger.error(f"删除文档失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"删除文档失败: {str(e)}"
                }
        
        @self.mcp.tool
        def aggregate(
            database: str, 
            collection: str,
            pipeline: List[Dict[str, Any]]
        ) -> Dict[str, Any]:
            """执行聚合管道"""
            try:
                result = self.mongo_manager.aggregate(database, collection, pipeline)
                return result.model_dump()
            except Exception as e:
                logger.error(f"执行聚合管道失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"执行聚合管道失败: {str(e)}"
                }
        
        @self.mcp.tool
        def create_index(
            database: str, 
            collection: str,
            keys: List, 
            name: str = None,
            unique: bool = False, 
            sparse: bool = False,
            background: bool = True
        ) -> Dict[str, Any]:
            """创建索引"""
            try:
                result = self.mongo_manager.create_index(
                    database, collection, keys, name, unique, sparse, background
                )
                return result.model_dump()
            except Exception as e:
                logger.error(f"创建索引失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"创建索引失败: {str(e)}"
                }
        
        @self.mcp.tool
        def list_indexes(database: str, collection: str) -> Dict[str, Any]:
            """列出集合的所有索引"""
            try:
                result = self.mongo_manager.list_indexes(database, collection)
                return result.model_dump()
            except Exception as e:
                logger.error(f"列出索引失败: {str(e)}")
                return {
                    "success": False,
                    "error": f"列出索引失败: {str(e)}"
                }
    
    async def run(self) -> None:
        """运行MCP服务器"""
        try:
            logger.info("启动MongoDB Atlas MCP服务器...")
            await self.mcp.run_stdio_async()
        except KeyboardInterrupt:
            logger.info("收到中断信号，正在关闭服务器...")
        finally:
            self.mongo_manager.close()
            logger.info("MongoDB Atlas MCP服务器已关闭")


def main():
    """主函数"""
    server = MongoAtlasMCPServer()
    return server


if __name__ == "__main__":
    server = main()
    asyncio.run(server.run()) 