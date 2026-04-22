"""
ColumnMetric 映射器

负责字段与指标关联关系的实体/模型转换，延续元数据模块统一的 Mapper
分层做法，避免上层直接依赖 ORM 细节
"""

from dataclasses import asdict

from app.entities.column_metric import ColumnMetric
from app.models.column_metric import ColumnMetricMySQL


class ColumnMetricMapper:
    """负责 `ColumnMetric` 与 `ColumnMetricMySQL` 之间的双向转换"""

    @staticmethod
    def to_entity(column_metric_mysql: ColumnMetricMySQL) -> ColumnMetric:
        """把关联关系 ORM 模型转换为业务实体"""
        return ColumnMetric(
            column_id=column_metric_mysql.column_id,
            metric_id=column_metric_mysql.metric_id,
        )

    @staticmethod
    def to_model(column_metric: ColumnMetric) -> ColumnMetricMySQL:
        """把关联关系业务实体转换为 ORM 模型"""
        return ColumnMetricMySQL(**asdict(column_metric))
