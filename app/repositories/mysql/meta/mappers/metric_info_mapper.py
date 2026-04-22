"""
MetricInfo 映射器

虽然本章重点是表与字段入库，但指标元数据也沿用同样的分层约定：
先以业务实体表达，再通过 Mapper 转成 ORM 模型
"""

from dataclasses import asdict

from app.entities.metric_info import MetricInfo
from app.models.metric_info import MetricInfoMySQL


class MetricInfoMapper:
    """负责 `MetricInfo` 与 `MetricInfoMySQL` 之间的双向转换"""

    @staticmethod
    def to_entity(model: MetricInfoMySQL) -> MetricInfo:
        """把指标 ORM 模型转换为业务实体"""
        return MetricInfo(
            id=model.id,
            name=model.name,
            description=model.description,
            relevant_columns=model.relevant_columns,
            alias=model.alias,
        )

    @staticmethod
    def to_model(entity: MetricInfo) -> MetricInfoMySQL:
        """把指标业务实体转换为 ORM 模型"""
        return MetricInfoMySQL(**asdict(entity))
