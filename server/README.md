# Office Work Automation Server

这是一个用于办公自动化的服务器项目，提供文档处理、用户信息管理等功能。

## 功能特性

- 用户信息管理（CRUD操作）
- 头像上传和管理
- docx文档自动填表
- xlsx表格自动填表
- RESTful API接口

## 目录结构

```
server/
├── app/                    # 应用程序主目录
│   ├── metadata_handler.py # 用户信息管理接口
│   └── ...                # 其他应用模块
├── config/                 # 配置文件目录
├── data/                   # 数据存储目录
│   └── persons/           # 用户信息JSON文件
├── lib/                    # 核心库
│   ├── error_response.py  # 错误响应处理
│   ├── docx_auto.py       # Word文档自动填表
│   └── xlsx_auto.py       # Excel表格自动填表
├── static/                 # 静态资源目录
│   └── img/               # 用户头像存储
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

2. 访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


