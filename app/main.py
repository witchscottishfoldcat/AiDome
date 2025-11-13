# app/main.py

import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# --- 1. 基础配置 (Boilerplate) ---
# 配置一个简单的日志记录器，以便我们在终端看到服务的运行状态。
# 这是保障系统可观测性的第一步。
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ArkHeart.Brain")


# --- 2. 创建FastAPI应用实例 (The Application Core) ---
# `app` 是我们整个Web服务的核心实例。
# 我们在这里为它添加了元数据，这有助于生成清晰的API文档。
app = FastAPI(
    title="ArkHeart Brain Service",
    description="The core AI service for the desktop companion, providing intelligence and state management.",
    version="0.1.0",
)


# --- 3. 定义WebSocket通信端点 (The Communication Gateway) ---
# 这是我们为“身体”(Frontend)敞开的唯一“大门”。
# GDD规定所有核心通信都通过WebSocket进行。
@app.websocket("/ws/v1/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    处理与单个“身体”客户端的WebSocket长连接。

    这个端点是实现 GDD 中“架构‘握手’原型”的关键。
    它负责：
    1. 接受一个合法的连接。
    2. 在整个连接生命周期内，监听并处理消息。
    3. 处理客户端断开连接的情况。
    """
    # 步骤 A: 接受连接
    await websocket.accept()
    logger.info(f"Connection established with client: {client_id}")

    try:
        # 步骤 B: 发送“握手成功”消息
        # 这是为了向客户端确认连接已成功建立。
        await websocket.send_json({
            "command_name": "handshake_response",
            "payload": {
                "accepted": True,
                "server_version": app.version,
                "message": f"Welcome, {client_id}. Brain connection successful."
            }
        })

        # 步骤 C: 进入主消息监听循环
        while True:
            # 等待从客户端接收消息。
            # 在原型阶段，我们只接收文本，未来将是JSON。
            received_data = await websocket.receive_text()
            logger.info(f"Received from {client_id}: {received_data}")

            # 原型功能：简单地将收到的消息“回声”返还给客户端。
            # 这是为了验证双向通信是通畅的。
            await websocket.send_json({
                "command_name": "echo_response",
                "payload": {
                    "original_message": received_data
                }
            })

    except WebSocketDisconnect:
        # 步骤 D: 处理客户端断开连接
        logger.warning(f"Client {client_id} has disconnected.")
    except Exception as e:
        # 步骤 E: 捕获意外错误
        logger.error(f"An unexpected error occurred with client {client_id}: {e}", exc_info=True)
        # 在实际应用中，我们可能需要在这里向Sentry等监控服务上报错误。


# --- 4. 定义HTTP健康检查端点 (The Health Check) ---
# 这是一个简单的HTTP接口，让我们可以从浏览器或监控工具
# 轻松地检查“大脑”服务是否还“活着”。
@app.get("/")
async def read_root():
    """
    提供一个基础的HTTP端点，用于确认服务正在运行。
    """
    return {"status": "ArkHeart Brain is alive and listening."}