"""
ORM 基类

定义项目中所有 SQLAlchemy ORM 模型共享的声明式基类
后续 table_info column_info metric_info 和 column_metric 都会继承这里的 Base
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """项目统一的 SQLAlchemy 声明式基类"""

    pass
