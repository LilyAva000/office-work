# OFFICE-WORK


## TODO

- [x] **前端引入 Zustand 进行状态管理**  
  使用 Zustand 实现全局状态持久化，提升用户体验，避免状态冗余。

- [x] **规范后端 API 错误管理**  
  已统一 API 错误响应格式，支持常见错误的集中处理和清晰提示，便于前端接入与日志追踪。

- [ ] **后端接入数据库**  
  当前使用 JSON 文件作为临时存储方案，需尽快替换为正式数据库（如 MySQL/PostgreSQL），以提升数据安全性、可扩展性与性能。

- [ ] **统一字段命名规范**  
  前后端字段命名存在差异（如 `persionID` / `persion_id` / `username` 等），建议制定统一命名规范，避免歧义和潜在 bug。

- [ ] **接入权限管理机制**  
  实现基于用户身份的权限控制，限制接口访问范围，支持普通用户与管理员角色区分。


## Web

<details>
<summary>前端环境依赖</summary>

**用法示例：**

```bash
cd web
npm install
npm install zustand
npx shadcn-ui@latest init
npx shadcn@latest init
```

</details>

完成依赖安装后，使用以下命令启动服务：

### 界面启动
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
