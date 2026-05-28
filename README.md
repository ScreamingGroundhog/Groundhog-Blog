# 个人博客系统

基于 **Vue 3 + Flask + MySQL** 构建的个人技术博客，支持 Markdown 编辑、代码高亮、数学公式渲染。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 (Composition API) + Vite + Pinia + Vue Router 4 + Tailwind CSS |
| Markdown | markdown-it + highlight.js + KaTeX |
| 后端 | Flask + Flask-SQLAlchemy + Flask-JWT-Extended |
| 数据库 | MySQL 8.x |
| 认证 | JWT |

## 功能

**前台（访客端）**
- 文章列表：分页、分类筛选、标签筛选
- 文章详情：Markdown 渲染、目录导航、代码块一键复制、图片点击放大、数学公式、上一篇/下一篇
- 全局搜索（标题 + 正文关键词）
- 关于我页面

**后台（管理端）**
- JWT 安全登录
- 文章管理：Markdown 编辑器（左右分栏实时预览）、发布/草稿/隐藏/置顶/删除
- 分类与标签管理
- 图片上传

## 项目结构

```
├── backend/              # Flask 后端
│   ├── app/
│   │   ├── __init__.py   # 应用工厂
│   │   ├── config.py     # 配置
│   │   ├── models.py     # 数据模型
│   │   └── routes/       # API 路由
│   ├── seed.py           # 初始化数据库
│   └── run.py            # 启动入口
├── frontend/             # Vue 3 前端
│   ├── src/
│   │   ├── api/          # Axios 封装
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── router/       # 路由配置
│   │   ├── components/   # 通用组件
│   │   └── views/        # 页面
│   └── package.json
└── README.md
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.x

### 1. 创建数据库

```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 配置后端

编辑 `backend/app/config.py` 中的数据库连接：

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_password@localhost:3306/blog_db"
```

或设置环境变量：

```bash
export DATABASE_URL="mysql+pymysql://root:your_password@localhost:3306/blog_db"
```

### 3. 启动后端

```bash
cd backend
pip install -r requirements.txt
python seed.py     # 初始化数据库 + 创建管理员
python run.py      # 启动 http://localhost:5000
```

默认管理员：`admin` / `admin123`

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev        # 启动 http://localhost:3000
```

前端开发服务器会自动将 `/api` 请求代理到后端 `http://localhost:5000`。

### 5. 访问

| 地址 | 说明 |
|------|------|
| http://localhost:3000 | 博客前台 |
| http://localhost:3000/admin | 管理后台 |
| http://localhost:3000/admin/login | 管理员登录 |

## API 接口

### 公开接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/public/articles` | 文章列表（分页、分类、标签、关键词） |
| GET | `/api/public/articles/:id` | 文章详情（含阅读计数） |
| GET | `/api/public/articles/:id/nearby` | 上一篇/下一篇 |
| GET | `/api/public/categories` | 分类列表 |
| GET | `/api/public/tags` | 标签列表 |
| GET | `/api/public/about` | 关于信息 |

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 登录 |
| POST | `/api/auth/register` | 注册 |
| GET | `/api/auth/me` | 获取当前用户 |
| PUT | `/api/auth/me` | 更新个人信息 |

### 管理接口（需 JWT）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/articles` | 文章列表 / 创建 |
| GET/PUT/DELETE | `/api/articles/:id` | 文章详情 / 更新 / 删除 |
| GET/POST | `/api/categories` | 分类列表 / 创建 |
| PUT/DELETE | `/api/categories/:id` | 更新 / 删除分类 |
| GET/POST | `/api/tags` | 标签列表 / 创建 |
| PUT/DELETE | `/api/tags/:id` | 更新 / 删除标签 |
| POST | `/api/files` | 上传文件 |
| GET | `/api/files/list` | 文件列表 |
| GET | `/api/files/:filename` | 获取文件 |
