"""
字段元数据业务实体

字段配置中的业务语义、从数仓补齐的真实类型，以及抽样得到的示例值，
都会汇总到这个对象里，再继续流向元数据库与后续检索链路
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ColumnInfo:
    """系统内部统一使用的字段元数据表达"""

    id: str
    name: str
    type: str
    role: str
    examples: list[Any]
    description: str
    alias: list[str]
    table_id: str
