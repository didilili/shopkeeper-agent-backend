"""
问数查询接口路由

负责定义前端访问的 `/api/query` 接口，并用流式响应模拟智能体执行过程。
本章先不接入真实 QueryService，重点是把 APIRouter、请求体解析和 SSE 返回格式串起来。
"""

import asyncio

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.api.schemas.query_schema import QuerySchema

# 当前模块只维护查询相关接口，避免后续所有 API 都挤在 main.py 中
query_router = APIRouter()


async def fake_streamer():
    """模拟智能体逐步返回执行进度的异步生成器"""

    # 先用 10 个 step 模拟执行过程，方便在浏览器或 Apifox 中观察流式效果
    for i in range(10):
        # 暂停 1 秒只是为了让流式返回更容易被观察；真实项目中这里会被节点耗时代替
        await asyncio.sleep(1)

        # SSE 每条消息以 data: 开头，并用两个换行符结束
        # StreamingResponse 会把每次 yield 的内容持续写给客户端
        yield f"data: step:{i}\n\n"


@query_router.post("/api/query")
async def query_handler(query: QuerySchema):
    """接收用户自然语言问题，并以 SSE 形式持续返回处理进度"""

    # query 参数由 FastAPI 根据请求体自动解析为 QuerySchema 对象
    # media_type 指定为 text/event-stream，前端才能按 SSE 流处理响应
    return StreamingResponse(fake_streamer(), media_type="text/event-stream")
