"""
字段取值业务实体

该对象用于承接字段值同步链路中的结构化结果，和表、字段、指标实体保持
一致的业务层表达方式
"""

from dataclasses import dataclass


@dataclass
class ValueInfo:
    """字段具体取值及其所属字段的业务表达"""

    id: str
    value: str
    column_id: str
