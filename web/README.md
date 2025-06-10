## "AI+” 档案管理

## 项目简介

“AI+”档案管理系统前端，基于 Next.js + React + Zustand + TailwindCSS 构建，支持个人档案信息的录入、编辑、保存及表格（Word/Excel）管理与预览。

---

## 目录结构说明

- `src/app/` ：页面路由（如 /login、/profile 等）
- `src/components/` ：UI 组件、表单、表格等复用组件
- `src/lib/` ：API 客户端、状态管理、工具函数
- `public/` ：静态资源（如表单模板、图片）
- `next.config.js` ：Next.js 配置
- `package.json` ：依赖与脚本

---

## 关键页面与功能

- **登录页面**  
  用户输入凭据登录系统，进入个人工作空间。

- **个人档案页面**  
  包含两个子模块：
  - **个人资料表单**：  
    显示用户基本信息，支持编辑与保存。初始数据应与 `form-template.json` 保持一致，用作信息模板。
  - **表格管理**：  
    提供 Word 与 Excel 文件的预览功能，便于用户查看已生成的填表文档。

### 登录页 `/login`

- 用户输入用户名、密码，调用后端 API 进行认证。
- 登录成功后自动获取用户信息并初始化全局状态。

### 个人档案页 `/profile`

- 个人资料表单：初始数据来自 `public/form-template.json`，支持分组编辑、保存、头像上传。
- 表格管理：自动获取后端表格列表，支持 Word/Excel 文件预览。
- 页面切换与状态提示友好。

### 组件说明

- `profile-form.tsx`：动态渲染表单，支持分组、子分组、字段校验、头像上传。
- `table-manager.tsx`：表格文件列表、文件选择与预览。
- `ui/` 目录：通用 UI 组件（Button、Input、Tabs、Toast、Dialog 等）。

---

## 状态管理与 API 交互

- 全局状态通过 `useUserStore`（Zustand）管理，包含用户信息、登录态、personId 等。
- API 调用统一封装于 `lib/apiClient.ts`，如登录、获取/更新用户信息、上传头像、获取表格列表等。
- 表单初始数据与结构由 `public/form-template.json` 提供，便于后端/前端协同扩展。

---

## 本地开发与启动

1. 安装依赖

```cmd
cd web
npm install
```

2. 初始化 UI 组件（如首次启动或组件库升级时）

```cmd
npx shadcn-ui@latest init
```

3. 启动开发服务器

```cmd
npm run dev
```

4. 访问 http://localhost:3000

如需修改默认端口，可参考以下方法：

<details>
<summary>修改 Next.js 默认端口</summary>

Next.js 默认开发端口为 `3000`，可通过命令行参数 `-p` 或 `--port` 修改：

```bash
npm run dev -- -p 3001
# 或
next dev -p 3001
```

也可以修改 package.json 中的 dev 脚本：
```bash
"scripts": {
  "dev": "next dev -p 3001"
}
```

生产环境启动（npm run start）同样支持 -p 参数：
```bash
npm run start -- -p 3001
```

</details>

---

## 主要技术栈

- Next.js 14 / React 18
- Zustand（全局状态管理）
- TailwindCSS（UI 设计）
- shadcn/ui（现代化 UI 组件）
- Radix UI（底层交互组件）
- Framer Motion（动画）

---

## 遵守规范

- 代码注释和类型定义较为完善，便于新成员快速上手。
- 代码风格统一，推荐遵循现有组件和 API 封装方式。
- 状态管理建议继续使用 Zustand，便于维护和扩展。
- 组件库基于 shadcn/ui，支持自定义主题和样式。
- 如需对接更多后端接口，建议统一在 `lib/apiClient.ts` 扩展。
- 表单结构可通过修改 `form-template.json` 灵活扩展，注意一定要和后端结构同步。

---

如有问题建议先查阅 `src/` 目录代码及本说明文档。
