# ArkHeart 项目开发者环境搭建与工作流指南 V2

本文档是新开发者加入项目的唯一入口。它包含了从零开始搭建完整开发环境（大脑+身体）的所有步骤。

## 1. 前置条件

1.  **Git:** 版本控制。
2.  **Python 3.10+:** [官方下载地址](https://www.python.org/downloads/)。
3.  **Poetry:** Python依赖管理工具。 [官方安装指南](https://python-poetry.org/docs/#installation)。
4.  **Godot Engine 4.x:** 游戏引擎。 [官方下载地址](https://godotengine.org/download/)。
    > **重要：** 为了在终端中能直接使用 `godot` 命令，请将Godot的可执行文件路径添加到您操作系统的环境变量 `PATH` 中。

## 2. 环境搭建（只需做一次）

### 第一步：克隆项目仓库

```bash
git clone [项目的Git仓库地址]
cd [项目文件夹]

第二步：安装所有依赖
我们使用 Makefile 来简化此过程。此命令将自动调用Poetry来安装所有Python库。

make install

3. 日常开发工作流
第一步：打开两个终端
为了同时运行“大脑”和“身体”，您需要打开两个独立的终端窗口，并将它们的当前目录都切换到项目根目录。

第二步：启动“大脑”
在第一个终端窗口中，运行以下命令：

make run-brain
您会看到Uvicorn服务器启动，并开始监听 http://127.0.0.1:8000。请保持此终端窗口开启。
第三步：启动“身体”
在第二个终端窗口中，运行以下命令：

make run-body
这会自动打开Godot编辑器并加载我们的“身体”项目。在Godot编辑器中，按 F5 即可运行。
