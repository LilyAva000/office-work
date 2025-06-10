# Office Work Automation Server

这是一个用于办公自动化的服务器项目，提供文档处理、用户信息管理等功能。

## 功能特性

- docx文档自动填表
- xlsx表格自动填表
- RESTful API接口
- 用户信息管理（CRUD操作）
- 权限管理（TODO）

## 目录结构

```
server/
├── app/                    # API业务接口与核心逻辑
│   ├── metadata_handler.py # 用户信息管理接口
│   └── ...                # 其他应用模块
├── config/                 # 配置文件目录
├── data/                   # JSON数据存储目录，要用数据库代替
│   ├── login/             # 用户账密信息
│   └── persons/           # 用户个人信息
├── lib/                    # 核心库
│   ├── docx_auto.py       # Word文档自动填表
│   └── xlsx_auto.py       # Excel表格自动填表
├── static/                 # 静态资源目录
│   └── logs/               # 日志文件
│   └── img/               # 用户头像存储
│   └── output/             # 自动填表导出路径
│   └── ...
├── templates/             # 文档模板目录
├── utils/                 # 通用工具函数
├── main.py               # 应用程序入口
└── requirements.txt      # 项目依赖
```

## 环境要求

- Python 3.10+
- FastAPI
- 其他依赖见 requirements.txt

## 安装步骤

1. 创建并激活虚拟环境：

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. 安装依赖：

```bash
uv pip install -r requirements.txt
```

## 启动服务

1. 启动主服务器：

```bash
python main.py
```

2. 访问 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 接口设计规范

- 所有 API 统一采用 `async def` + `aiofiles` 实现异步 IO，提升高并发性能。
- 响应格式统一，所有接口返回如下结构：
  ```json
  {
    "code": 200,
    "msg": "操作成功",
    "data": { ... }
  }
  ```
- 错误码与错误信息集中配置于 `config/error_config.yaml`，便于维护和前后端联调，状态码可参考[HTTP 响应状态码](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Status)。
- 全局异常处理见 `app/api_common.py`，保证所有异常均有结构化响应。
- 主要业务接口见 `app/user_handler.py`、`app/table_handler.py`、`app/metadata_handler.py`。

## TODO

- [x] **统一 API 错误处理机制**  
      已实现全局异常处理，所有接口错误响应结构统一。  
      📄 相关文件：`app/api_common.py` 及各 handler 模块

---

- [ ] **接入 PostgreSQL 数据库替代 JSON 存储**  
      将当前基于文件系统的 JSON 存储方案全面替换为数据库，提升数据的安全性、扩展性与统一管理能力。
  - `data/persons/` 目录下的信息需迁移至数据库
  - API接口的相关逻辑均需改造为数据库操作

---

- [ ] **完善用户认证与权限体系**  
      构建统一的权限控制逻辑，满足实际使用中的角色区分与数据保护需求。包括：
  - 登录接口返回用户唯一标识 ID，便于前端全局识别与鉴权
  - 批量填表接口增加管理员权限校验
  - 模板管理接口仅允许超级管理员访问

---

- [ ] **补全代码内 TODO 实现项**  
      检查项目代码中的 `# TODO` 注释，逐项确认并完善未完成逻辑与功能实现。
