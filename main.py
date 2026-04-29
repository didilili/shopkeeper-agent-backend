"""
FastAPI 应用入口

负责创建后端应用实例，并把各业务模块中的 router 挂载到同一个 app 上。
本章先只注册问数查询接口，后续 lifespan、middleware、Depends 等工程能力
也会从这里逐步接入。
"""

from fastapi import FastAPI

from app.api.routers.query_router import query_router

# 创建 FastAPI 应用对象，所有路由、中间件和生命周期事件最终都会注册到这里
app = FastAPI()

# 把查询路由注册进应用；没有挂载时，/docs 和真实 HTTP 请求都访问不到该接口
app.include_router(query_router)
