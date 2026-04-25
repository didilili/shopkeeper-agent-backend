"""
元数据知识库构建脚本入口

相当于构建流程的 controller 层，负责接收命令行参数 初始化客户端 创建仓储和服务对象
再把真正的构建任务调度到 MetaKnowledgeService，它本身不承载复杂业务细节
主要目标是把整条构建链路稳定地启动起来
"""

import argparse
import asyncio
from pathlib import Path

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import (
    dw_mysql_client_manager,
    meta_mysql_client_manager,
)
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.meta_knowledge_service import MetaKnowledgeService


async def build(config_path: Path):
    """初始化依赖并执行一次元数据知识构建"""

    # 初始化元数据MySQL客户端
    meta_mysql_client_manager.init()
    # 初始化数据仓库MySQL客户端
    dw_mysql_client_manager.init()
    # 初始化Qdrant客户端
    qdrant_client_manager.init()
    # 初始化Embedding客户端
    embedding_client_manager.init()
    # 初始化Elasticsearch客户端
    es_client_manager.init()

    async with (
        meta_mysql_client_manager.session_factory() as meta_session,
        dw_mysql_client_manager.session_factory() as dw_session,
    ):
        # 创建 repository 对象
        meta_mysql_repository = MetaMySQLRepository(meta_session)
        dw_mysql_repository = DWMySQLRepository(dw_session)
        # 字段和指标分别写入不同的 Qdrant collection，后续可以独立召回
        column_qdrant_repository = ColumnQdrantRepository(qdrant_client_manager.client)
        embedding_client = embedding_client_manager.client
        value_es_repository = ValueESRepository(es_client_manager.client)
        metric_qdrant_repository = MetricQdrantRepository(qdrant_client_manager.client)

        # 创建 service 对象，并把 repository 注入进去
        meta_knowledge_service = MetaKnowledgeService(
            meta_mysql_repository=meta_mysql_repository,
            dw_mysql_repository=dw_mysql_repository,
            column_qdrant_repository=column_qdrant_repository,
            embedding_client=embedding_client,
            value_es_repository=value_es_repository,
            metric_qdrant_repository=metric_qdrant_repository,
        )

        # 真正进入服务层的构建逻辑
        await meta_knowledge_service.build(config_path)

    # 结束后关闭客户端连接
    await meta_mysql_client_manager.close()
    await dw_mysql_client_manager.close()
    await qdrant_client_manager.close()
    await es_client_manager.close()


if __name__ == "__main__":
    # 解析命令行参数，由外部决定本次构建使用哪份配置文件
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True)
    args = parser.parse_args()

    # 将字符串路径转成 Path，再启动异步 build
    asyncio.run(build(Path(args.conf)))
