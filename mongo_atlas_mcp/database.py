"""
MongoDB Atlas 数据库连接和操作核心类

提供MongoDB Atlas的连接管理和基本操作功能
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

from .models import (
    DatabaseInfo, CollectionInfo, IndexInfo, MongoResponse
)

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoAtlasManager:
    """
    MongoDB Atlas 管理器
    
    负责MongoDB Atlas的连接管理和基本操作
    """
    
    def __init__(self):
        """初始化MongoDB Atlas管理器"""
        self.client: Optional[MongoClient] = None
        self._connect()
    
    def _connect(self) -> None:
        """
        连接到MongoDB Atlas
        
        从环境变量读取连接字符串并建立连接
        """
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
    
    def get_database(self, database_name: str) -> Database:
        """
        获取数据库对象
        
        Args:
            database_name: 数据库名称
            
        Returns:
            Database对象
        """
        if not self.client:
            raise ConnectionError("MongoDB客户端未连接")
        return self.client[database_name]
    
    def get_collection(self, database_name: str, collection_name: str) -> Collection:
        """
        获取集合对象
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            
        Returns:
            Collection对象
        """
        database = self.get_database(database_name)
        return database[collection_name]
    
    def list_databases(self) -> MongoResponse:
        """
        列出所有数据库
        
        Returns:
            包含数据库列表的响应对象
        """
        try:
            databases = []
            for db_name in self.client.list_database_names():
                # 只获取数据库名称，不执行需要管理员权限的命令
                database_info = DatabaseInfo(
                    name=db_name,
                    size_on_disk=0,  # 不获取大小信息，避免权限问题
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
    
    def list_collections(self, database_name: str) -> MongoResponse:
        """
        列出指定数据库的所有集合
        
        Args:
            database_name: 数据库名称
            
        Returns:
            包含集合列表的响应对象
        """
        try:
            database = self.get_database(database_name)
            collections = []
            
            for collection_name in database.list_collection_names():
                # 只获取集合名称，不执行需要管理员权限的命令
                collection_info = CollectionInfo(
                    name=collection_name,
                    count=0,  # 不获取文档数量，避免权限问题
                    size=0,   # 不获取大小信息，避免权限问题
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
    
    def find_documents(self, database_name: str, collection_name: str, 
                      filter_dict: Dict[str, Any] = None, 
                      projection: Dict[str, Any] = None,
                      sort: List[tuple] = None,
                      limit: int = None,
                      skip: int = 0) -> MongoResponse:
        """
        查询文档
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            filter_dict: 查询过滤器
            projection: 投影字段
            sort: 排序规则
            limit: 限制返回数量
            skip: 跳过文档数量
            
        Returns:
            包含查询结果的响应对象
        """
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
    
    def insert_document(self, database_name: str, collection_name: str, 
                       document: Dict[str, Any]) -> MongoResponse:
        """
        插入文档
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            document: 要插入的文档
            
        Returns:
            包含插入结果的响应对象
        """
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
    
    def update_document(self, database_name: str, collection_name: str,
                       filter_dict: Dict[str, Any], update_dict: Dict[str, Any],
                       upsert: bool = False, multi: bool = False) -> MongoResponse:
        """
        更新文档
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            filter_dict: 更新过滤器
            update_dict: 更新操作
            upsert: 是否插入不存在文档
            multi: 是否更新多个文档
            
        Returns:
            包含更新结果的响应对象
        """
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
    
    def delete_document(self, database_name: str, collection_name: str,
                       filter_dict: Dict[str, Any], multi: bool = False) -> MongoResponse:
        """
        删除文档
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            filter_dict: 删除过滤器
            multi: 是否删除多个文档
            
        Returns:
            包含删除结果的响应对象
        """
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
    
    def aggregate(self, database_name: str, collection_name: str,
                  pipeline: List[Dict[str, Any]]) -> MongoResponse:
        """
        执行聚合管道
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            pipeline: 聚合管道
            
        Returns:
            包含聚合结果的响应对象
        """
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
    
    def create_index(self, database_name: str, collection_name: str,
                     keys: List[tuple], name: str = None,
                     unique: bool = False, sparse: bool = False,
                     background: bool = True) -> MongoResponse:
        """
        创建索引
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            keys: 索引键
            name: 索引名称
            unique: 是否唯一索引
            sparse: 是否稀疏索引
            background: 是否后台创建
            
        Returns:
            包含创建索引结果的响应对象
        """
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
    
    def list_indexes(self, database_name: str, collection_name: str) -> MongoResponse:
        """
        列出集合的所有索引
        
        Args:
            database_name: 数据库名称
            collection_name: 集合名称
            
        Returns:
            包含索引列表的响应对象
        """
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
    
    def close(self) -> None:
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            logger.info("MongoDB连接已关闭") 