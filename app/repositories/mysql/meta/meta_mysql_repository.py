"""
元数据库 MySQL 仓储

这一层对应文档里的 Meta Repository，负责接收业务实体并落到 Meta MySQL
Repository 自身只关心“如何写入”，而“哪些写操作要放在同一笔事务里”，由 Service 层统一决定

表 字段 指标和字段指标关系都会先以业务实体流转，再在这里统一转成 ORM 模型
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.column_info import ColumnInfo
from app.entities.column_metric import ColumnMetric
from app.entities.metric_info import MetricInfo
from app.entities.table_info import TableInfo
from app.repositories.mysql.meta.mappers.column_info_mapper import ColumnInfoMapper
from app.repositories.mysql.meta.mappers.column_metric_mapper import ColumnMetricMapper
from app.repositories.mysql.meta.mappers.metric_info_mapper import MetricInfoMapper
from app.repositories.mysql.meta.mappers.table_info_mapper import TableInfoMapper


class MetaMySQLRepository:
    """负责把元数据业务实体持久化到 Meta MySQL"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def save_table_infos(self, table_infos: list[TableInfo]):
        """批量保存表元数据。输入仍然是业务实体，而不是 ORM 模型"""
        self.session.add_all(
            [TableInfoMapper.to_model(table_info) for table_info in table_infos]
        )

    def save_column_infos(self, column_infos: list[ColumnInfo]):
        """批量保存字段元数据。实体到模型的转换统一通过 Mapper 完成"""
        self.session.add_all(
            [ColumnInfoMapper.to_model(column_info) for column_info in column_infos]
        )

    def save_metric_infos(self, metric_infos: list[MetricInfo]):
        """批量保存指标元数据。指标本身和字段关联关系分开写入"""
        self.session.add_all(
            [MetricInfoMapper.to_model(metric_info) for metric_info in metric_infos]
        )

    def save_column_metrics(self, column_metrics: list[ColumnMetric]):
        """批量保存字段与指标的关联关系"""
        self.session.add_all(
            [
                ColumnMetricMapper.to_model(column_metric)
                for column_metric in column_metrics
            ]
        )
