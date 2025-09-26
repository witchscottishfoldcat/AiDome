# FastAPI Project

A modern, scalable FastAPI application with a well-structured architecture.

## Project Structure

```
project_name/
├── app/                 # FastAPI应用入口
│   ├── __init__.py
│   └── main.py
├── config/              # 配置文件
│   ├── __init__.py
│   └── settings.py
├── database.py          # 数据库配置
├── api/                 # API相关代码
│   ├── __init__.py
│   ├── deps.py          # 依赖注入
│   └── v1/              # API版本控制
│       ├── __init__.py
│       ├── router.py    # 路由汇总
│       └── endpoints/   # API端点
│           ├── __init__.py
│           ├── auth.py
│           ├── users.py
│           └── items.py
├── core/                # 核心模块
│   ├── __init__.py
│   ├── security.py      # 认证授权
│   ├── exceptions.py    # 自定义异常
│   └── middleware.py    # 中间件
├── models/              # 数据库模型
│   ├── __init__.py
│   ├── base.py          # 基础模型
│   ├── user.py
│   └── item.py
├── schemas/             # Pydantic模型
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── services/            # 业务逻辑层
│   ├── __init__.py
│   ├── user_service.py
│   └── item_service.py
├── utils/               # 工具函数
│   ├── __init__.py
│   ├── validators.py    # 验证器
│   └── helpers.py       # 工具函数
├── tests/               # 测试文件
│   ├── __init__.py
│   ├── conftest.py      # pytest配置
│   ├── test_auth.py
│   └── test_users.py
├── migrations/          # 数据库迁移文件
├── scripts/             # 部署和工具脚本
├── docs/                # 项目文档
├── requirements/        # 依赖管理
│   ├── base.txt         # 基础依赖
│   ├── dev.txt          # 开发依赖
│   └── prod.txt         # 生产依赖
├── .env.example         # 环境变量示例
├── Dockerfile
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```

### Running the Application

```bash
uvicorn app.main:app --reload
```

## Configuration

Copy `.env.example` to `.env` and configure your environment variables.

## Testing

Run tests with pytest:

```bash
pytest
```

## Deployment

Use Docker to deploy the application:

```bash
docker-compose up -d
```