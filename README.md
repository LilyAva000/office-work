# OFFICE-WORK


## TODO

- 后端接入数据库：
  - 目前采用 JSON 文件存储数据，仅作为临时过渡方案。
  - 需尽快设计并集成正式的数据库（如 MySQL、PostgreSQL 等），以提升数据安全性和扩展性。

- 规范后端 API 错误管理：
  - 统一 API 错误响应格式，便于前端处理和日志追踪。
  - 拦截和处理常见、已知错误，输出明确的错误信息，方便快速定位和修复问题。

- 命名规范统一：
  - 前后端需注意因未引入数据库导致的命名不一致问题（如 persionID、persion_id、username 等）。
  - 建议制定统一的字段命名规范，避免歧义和潜在 bug。

- 前端引入 Zustand 作为状态管理辅助：
  - 使用 Zustand 实现全局状态管理，并支持持久化存储，提升用户体验。
  - 参考官方文档，合理划分状态模块，避免冗余和重复。

如有新任务或建议，请及时补充。

## Web

请前往 [web/README.md](web/README.md) 查看前端项目的详细说明。

请确保已完成依赖安装后，使用以下命令启动服务：

```bash
cd web
npm run dev
```

## Server

### 环境依赖

<details>
<summary>Windows</summary>

**用法示例：**

```bash
cd server
uv venv .venv --python=3.11
.venv\Scripts\activate
uv pip install -r requirements.txt
```

</details>

<details>
<summary>Linux</summary>

**用法示例：**

```bash
cd server
uv venv .venv --python=3.11
source .venv/bin/activate
uv pip install -r requirements.txt
```

</details>

### 服务启动

请确保已完成依赖安装后，使用以下命令启动服务：

```bash
cd server
python main.py
```

启动后，可通过以下地址访问 API 文档：

- [Swagger UI](http://127.0.0.1:8008/docs#/)
- [ReDoc](http://127.0.0.1:8008/redoc)
