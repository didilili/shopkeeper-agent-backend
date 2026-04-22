"""
TableInfo 映射器

负责在表元数据业务实体和 ORM 模型之间做双向转换，让 Service/Repository
不需要直接操作 SQLAlchemy 模型
"""

from dataclasses import asdict

from app.entities.table_info import TableInfo
from app.models.table_info import TableInfoMySQL


class TableInfoMapper:
    """负责 `TableInfo` 与 `TableInfoMySQL` 之间的双向转换"""

    @staticmethod
    def to_entity(table_info_mysql: TableInfoMySQL) -> TableInfo:
        """把 ORM 模型还原成业务实体，便于上层业务逻辑继续流转"""
        return TableInfo(
            id=table_info_mysql.id,
            name=table_info_mysql.name,
            role=table_info_mysql.role,
            description=table_info_mysql.description,
        )

    @staticmethod
    def to_model(table_info: TableInfo) -> TableInfoMySQL:
        """把业务实体转换成 ORM 模型，交给 SQLAlchemy 托管"""
        return TableInfoMySQL(**asdict(table_info))
