"""
MongoDB Atlas MCP 数据模型

定义请求和响应的数据结构
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field


class DatabaseInfo(BaseModel):
    """数据库信息模型"""
    name: str = Field(..., description="数据库名称")
    size_on_disk: Optional[int] = Field(None, description="数据库大小（字节）")
    empty: Optional[bool] = Field(None, description="是否为空")


class CollectionInfo(BaseModel):
    """集合信息模型"""
    name: str = Field(..., description="集合名称")
    count: Optional[int] = Field(None, description="文档数量")
    size: Optional[int] = Field(None, description="集合大小（字节）")
    avg_obj_size: Optional[int] = Field(None, description="平均对象大小")


class IndexInfo(BaseModel):
    """索引信息模型"""
    name: str = Field(..., description="索引名称")
    key: List[Dict[str, Union[str, int]]] = Field(..., description="索引键")
    unique: bool = Field(False, description="是否唯一索引")
    sparse: bool = Field(False, description="是否稀疏索引")
    background: bool = Field(True, description="是否后台创建")


class FindDocumentsRequest(BaseModel):
    """查询文档请求模型"""
    database: str = Field(..., description="数据库名称")
    collection: str = Field(..., description="集合名称")
    filter: Optional[Dict[str, Any]] = Field({}, description="查询过滤器")
    projection: Optional[Dict[str, Any]] = Field(None, description="投影字段")
    sort: Optional[List[tuple]] = Field(None, description="排序规则")
    limit: Optional[int] = Field(None, description="限制返回数量")
    skip: Optional[int] = Field(0, description="跳过文档数量")


class InsertDocumentRequest(BaseModel):
    """插入文档请求模型"""
    database: str = Field(..., description="数据库名称")
    collection: str = Field(..., description="集合名称")
    document: Dict[str, Any] = Field(..., description="要插入的文档")


class UpdateDocumentRequest(BaseModel):
    """更新文档请求模型"""
    database: str = Field(..., description="数据库名称")
    collection: str = Field(..., description="集合名称")
    filter: Dict[str, Any] = Field(..., description="更新过滤器")
    update: Dict[str, Any] = Field(..., description="更新操作")
    upsert: bool = Field(False, description="是否插入不存在文档")
    multi: bool = Field(False, description="是否更新多个文档")


class DeleteDocumentRequest(BaseModel):
    """删除文档请求模型"""
    database: str = Field(..., description="数据库名称")
    collection: str = Field(..., description="集合名称")
    filter: Dict[str, Any] = Field(..., description="删除过滤器")


class AggregateRequest(BaseModel):
    """聚合管道请求模型"""
    database: str = Field(..., description="数据库名称")
    collection: str = Field(..., description="集合名称")
    pipeline: List[Dict[str, Any]] = Field(..., description="聚合管道")


class CreateIndexRequest(BaseModel):
    """创建索引请求模型"""
    database: str = Field(..., description="数据库名称")
    collection: str = Field(..., description="集合名称")
    keys: List[tuple] = Field(..., description="索引键")
    name: Optional[str] = Field(None, description="索引名称")
    unique: bool = Field(False, description="是否唯一索引")
    sparse: bool = Field(False, description="是否稀疏索引")
    background: bool = Field(True, description="是否后台创建")


class MongoResponse(BaseModel):
    """MongoDB操作响应模型"""
    success: bool = Field(..., description="操作是否成功")
    data: Optional[Any] = Field(None, description="响应数据")
    error: Optional[str] = Field(None, description="错误信息")
    count: Optional[int] = Field(None, description="影响文档数量") 