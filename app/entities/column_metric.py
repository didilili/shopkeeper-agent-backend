"""
字段与指标关联业务实体

用于表达一个指标依赖哪些字段，为后续指标知识组织和关联查询提供统一的中间对象
"""

from dataclasses import dataclass


@dataclass
class ColumnMetric:
    """字段和指标之间的关联关系"""

    column_id: str
    metric_id: str
