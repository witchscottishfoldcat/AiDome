# 方舟之心：AI核心 "大脑" (Project ArkHeart: The AI Core "Brain")

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codestyle: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**方舟之心 (ArkHeart)** 是 AI 桌面宠物“方舟”项目的核心智能中枢。它是一个运行在本地的、事件驱动的、高度模块化的服务，负责驱动宠物的所有行为、记忆、情感和进化。

**⚠️ 重要：本项目并非一个独立的应用程序。** 它必须与“**方舟之躯 (ArkBody - 前端)**”和“**方舟启动器 (ArkLauncher)**”协同工作，共同构成完整的桌面宠物体验。

> 我们的创世蓝图，详细阐述了每一个设计决策背后的“为什么”。在贡献代码或进行深度定制前，请务必阅读：
> **[《AI桌面宠物 · 创世设计文档》](./docs/Genesis_Design_Document.md)**

---

## ✨ 核心架构哲学 (Core Architectural Philosophy)

本项目并非一个传统的CRUD Web应用，它被设计为一个**可持续进化的、事件驱动的认知架构**。

- **🧠 大脑/身体/启动器分离:** 通过物理或逻辑进程分离，实现了智能、表现和管理的极致解耦。
- **⚡ 事件驱动:** 所有内部模块均通过一个中央“事件总线”进行异步通信，杜绝了模块间的硬编码依赖。
- **🧩 高内聚、低耦合:** 每个模块都像一个独立的“微服务”，只专注于单一职责（IO, 状态管理, 决策等）。
- **📜 契约优先:** 所有内外部通信都由严格的、版本化的API契约来定义，是多语言协作和长期维护的基石。

## 📂 项目结构导览 (Project Structure Navigation)

ark_heart/
├── app/ # FastAPI 应用入口与核心服务 (如事件总线)
├── api/ # 对外通信接口 (WebSocket, HTTP调试接口)
├── core/ # 🧠 AI的心智内核 (决策、状态、心智健康)
│ └── README.md # <<-- 了解AI如何思考，请从这里开始
├── services/ # 🔌 连接外部世界的感官与喉舌 (IO适配层)
│ └── README.md # <<-- 了解如何更换LLM/TTS/记忆库，请从这里开始
├── plugins/ # 🛠️ 可插拔的技能工具箱
│ └── README.md # <<-- 【社区贡献者必读】了解如何编写新技能，请从这里开始
├── schemas/ # 📜 系统的通用语言与数据契约
│ └── README.md # <<-- 了解所有事件和数据结构定义，请从这里开始
├── config/ # 🎛️ 人格与系统的总控制台
│ └── README.md # <<-- 【调教师必读】了解所有可配置参数，请从这里开始
├── tests/ # 🔬 自动化测试，保障系统稳定
├── docs/ # 📄 项目的核心设计文档
├── requirements/ # Python 依赖管理
├── .env.example # 环境变量示例
├── Dockerfile # 用于生产部署的容器化配置
└── docker-compose.yml # 用于本地开发的一键启动环境

## 🚀 快速上手 (Getting Started)

### 1. 先决条件
- Python 3.10+
- [Poetry](https://python-poetry.org/) (推荐的依赖与虚拟环境管理工具)
- [Docker](https://www.docker.com/) 和 Docker Compose (**最简单**的启动方式)

### 2. (推荐) 使用Docker一键启动
这是最简单的启动方式，它会自动拉取并运行Python环境和MemU服务。

1.  **配置环境：**
    - 复制 `.env.example` 为 `.env`。
    - 在 `.env` 文件中填入你的 `OPENAI_API_KEY` 等必要的密钥。

2.  **启动服务：**
    ```bash
    docker-compose up -d --build
    ```
    “大脑”将在 `ws://localhost:8000/ws` 等待“身体”的连接。

### 3. (手动) 本地开发环境设置

1.  **克隆仓库**
    ```bash
    git clone https://github.com/your-repo/ark-heart.git
    cd ark-heart
    ```
2.  **安装MemU服务**
    - 请遵循 [MemU官方文档](https://memu.pro) 的指引，下载并启动MemU服务。确保它正在 `http://localhost:8001` (或你在`.env`中配置的地址) 运行。
3.  **安装Python依赖**
    ```bash
    poetry install
    ```
4.  **配置环境变量** (同Docker方式)
5.  **启动“大脑”**
    ```bash
    poetry run uvicorn app.main:app --reload --port 8000
    ```

## 🧪 运行测试 (Running Tests)
本项目采用`pytest`进行全面的自动化测试。测试覆盖了核心模块的单元测试和使用模拟（Mocks）的集成测试。
```bash
poetry run pytest