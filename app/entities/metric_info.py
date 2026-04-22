"""
指标元数据业务实体

本章主线暂未深入到指标链路，但指标实体沿用了与表、字段一致的业务对象
表达方式，方便后续扩展到指标入库和检索
"""

from dataclasses import dataclass


@dataclass
class MetricInfo:
    """系统内部统一使用的指标元数据表达"""

    id: str
    name: str
    description: str
    relevant_columns: list[str]
    alias: list[str]
