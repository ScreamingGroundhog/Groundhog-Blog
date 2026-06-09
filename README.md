# 个人博客系统

基于 **Vue 3 + Flask + MySQL** 构建的个人技术博客，支持 Markdown 编辑、代码高亮、数学公式渲染。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 (Composition API) + Vite + Pinia + Vue Router 4 + Tailwind CSS |
| Markdown | markdown-it + highlight.js + KaTeX |
| 后端 | Flask + Flask-SQLAlchemy + Flask-JWT-Extended |
| 数据库 | MySQL 8.x / 9.x |
| 认证 | JWT |

> **新手导读：这些技术分别是做什么的？**
>
> **前端（用户看到的网页界面）**
> - **Vue 3**：前端框架。你可以把它理解为"搭网页积木"的工具——把页面拆成一个个可复用的组件，然后像拼乐高一样拼出完整的页面。Composition API 是 Vue 3 的新写法，更灵活。
> - **Vite**：前端构建工具。负责三件事：① 开发时启动一个本地服务器让你能实时预览网页；② 代码改动后自动刷新浏览器（热更新）；③ 打包时把代码压缩优化，生成最终给用户访问的静态文件。
> - **Pinia**：状态管理库。解决"不同页面组件之间怎么共享数据"的问题。比如用户登录后，导航栏和文章列表都需要知道当前用户是谁，Pinia 就是用来存这些全局共享的数据的。
> - **Vue Router**：路由库。负责管理页面跳转——用户访问 `/admin` 就显示管理后台，访问 `/` 就显示博客首页。本质上是把 URL 路径映射到对应的页面组件。
> - **Tailwind CSS**：CSS 框架。不需要你写 CSS 文件，直接在 HTML 标签上用简短的 class 名控制样式。比如 `class="bg-white p-4 rounded"` 就表示"白色背景、内边距、圆角"。
>
> **Markdown 渲染（文章排版）**
> - **markdown-it**：将 Markdown 文本转换为 HTML。你写的 `# 标题` 会变成 `<h1>标题</h1>`。
> - **highlight.js**：代码语法高亮。自动检测代码块中的语言（Python、JS 等），给关键词上色。
> - **KaTeX**：数学公式渲染。支持 LaTeX 语法的公式，比如 `$$E=mc^2$$` 会渲染成漂亮的数学公式。
>
> **后端（服务器端的逻辑处理）**
> - **Flask**：Python 的轻量级 Web 框架。负责接收前端的请求、处理业务逻辑、返回数据。所谓"轻量级"意味着它只提供最核心的功能，其他功能通过扩展（插件）来添加。
> - **Flask-SQLAlchemy**：数据库工具。让你用 Python 代码操作数据库，而不用手写 SQL 语句。比如 `Article.query.filter_by(category_id=1).all()` 等价于 `SELECT * FROM articles WHERE category_id=1`。
> - **Flask-JWT-Extended**：JWT 认证插件。JWT（JSON Web Token）是一种安全的身份验证方式——用户登录后服务器发一个加密的"令牌"，后续请求带上这个令牌，服务器就知道"这是谁"了，不用每次都输密码。
> - **Flask-CORS**：跨域请求处理。前端运行在 `localhost:3000`，后端运行在 `localhost:5000`，浏览器默认会阻止这种跨端口请求，CORS 插件告诉浏览器"这个跨域请求是允许的"。
>
> **数据库**
> - **MySQL**：关系型数据库。数据以表格形式存储，不同的表之间可以通过外键关联。比如"文章表"关联"分类表"和"标签表"。（本项目也兼容 MariaDB）
> - **PyMySQL**：Python 连接 MySQL 的驱动。Flask 通过它来和 MySQL 数据库通信。

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
├── backend/              # Flask 后端（Python）
│   ├── app/
│   │   ├── __init__.py   # 应用工厂：创建并配置 Flask 应用实例
│   │   ├── config.py     # 配置：数据库地址、JWT 密钥、上传文件限制等
│   │   ├── models.py     # 数据模型：定义数据库表结构（文章、分类、标签、用户）
│   │   └── routes/       # API 路由：定义所有接口（前端通过这里获取/提交数据）
│   ├── seed.py           # 初始化脚本：建表 + 插入默认分类/标签 + 创建管理员
│   ├── run.py            # 启动入口：运行此文件即可启动后端服务
│   ├── uploads/          # 上传文件存储目录
│   ├── requirements.txt  # Python 依赖清单（类似 package.json）
│   └── .env              # 环境变量配置（密钥、数据库密码等敏感信息）
├── frontend/             # Vue 3 前端（JavaScript）
│   ├── src/
│   │   ├── api/          # Axios 封装：定义所有向后端发请求的函数
│   │   ├── stores/       # Pinia 状态管理：存储登录状态等全局数据
│   │   ├── router/       # 路由配置：定义 URL 路径与页面的对应关系
│   │   ├── components/   # 通用组件：导航栏、分页器等可复用的 UI 块
│   │   └── views/        # 页面：首页、文章详情、管理后台等完整页面
│   ├── index.html        # HTML 入口：Vue 应用挂载到这个页面
│   ├── vite.config.js    # Vite 配置：端口号、代理规则
│   ├── package.json      # 前端依赖清单（Node.js 项目标准文件）
│   └── tailwind.config.js # Tailwind CSS 配置
└── README.md
```

> **新手导读：前后端是如何协作的？**
>
> 整个系统的运作流程可以概括为：**浏览器 ← 通过 API → 后端 ← 读写 → 数据库**
>
> 1. 用户在浏览器访问 `http://localhost:3000`，浏览器加载前端页面（Vue 编译后的 HTML+JS+CSS）。
> 2. 前端页面加载后，Vue 代码通过 Axios 向后端发送 HTTP 请求获取数据（比如 `GET /api/public/articles` 获取文章列表）。
> 3. 后端 Flask 收到请求后，通过 SQLAlchemy 查询 MySQL 数据库，拿到数据，以 JSON 格式返回给前端。
> 4. Vue 拿到 JSON 数据后，把数据渲染成用户看到的网页内容。
>
> **为什么开发时访问的是 3000 端口而不是 5000？** 因为 Vite 开发服务器（端口 3000）内置了代理功能——当你访问 `localhost:3000/api/xxx` 时，Vite 会自动把这个请求转发到后端 `localhost:5000/api/xxx`，然后把结果返回给你。这样做的好处是避免了浏览器的跨域限制。

## 快速开始

### 环境要求

- Python 3.10+（用来运行后端）
- Node.js 18+（用来运行前端，安装后自带 npm 包管理器）
- MySQL 8.x / 9.x（数据库，也可以使用 MariaDB）

### 1. 初始化并启动 MySQL

> 如果已经安装过 MySQL 且服务正在运行，跳过这一步，直接创建数据库即可。

MySQL 刚刚安装时，数据目录是空的，需要先初始化才能启动服务：

```bash
# 初始化数据目录（只在第一次安装后需要执行）
sudo mysqld --initialize --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# 启动 MySQL 服务
sudo systemctl start mysqld

# 设置开机自启（可选）
sudo systemctl enable mysqld
```

初始化后 MySQL 会生成一个临时密码，找到它并完成安全设置：

```bash
# 查看临时密码
sudo grep 'temporary password' /var/lib/mysql/*.err

# 使用临时密码登录，然后修改 root 密码、移除匿名用户等
sudo mysql_secure_installation
```

然后创建项目需要的数据库：

```sql
-- 登录 MySQL 后执行
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

> **utf8mb4 是什么？** MySQL 的 utf8 编码只能存 3 字节的字符（不支持 emoji 和部分生僻字），utf8mb4 支持完整的 4 字节 UTF-8 字符，能存 emoji 表情等特殊字符。`COLLATE utf8mb4_unicode_ci` 指定了排序和比较规则。

### 2. 配置后端

后端通过 `.env` 文件读取敏感配置（数据库密码、密钥等），而不是把这些信息硬编码在代码里：

```bash
cd backend
cp .env.example .env    # 从模板复制一份
```

编辑 `.env` 文件，修改数据库连接密码为你自己设置的密码：

```env
SECRET_KEY=你的密钥（随便写一串随机字符就行）
JWT_SECRET_KEY=你的JWT密钥（同样随便写）
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/blog_db
```

> **这个 URL 是什么意思？** `mysql+pymysql://` 表示用 pymysql 驱动连接 MySQL；`root:你的密码` 是用户名和密码；`@localhost:3306/blog_db` 是数据库地址、端口和库名。

### 3. 启动后端

```bash
cd backend

# 创建虚拟环境（隔离项目依赖，避免和系统其他 Python 项目冲突）
python3 -m venv venv

# 激活虚拟环境（之后 pip install 都会安装到这个隔离环境里）
source venv/bin/activate

# 安装项目依赖（Flask、SQLAlchemy 等）
# 每次添加新依赖后需要重新执行
pip install -r requirements.txt

# 初始化数据库表结构 + 插入示例数据 + 创建管理员账号
python seed.py

# 启动后端服务 http://localhost:5000
python run.py
```

> **什么是虚拟环境？** 不同 Python 项目可能需要不同版本的库（比如项目 A 需要 Flask 3.0，项目 B 需要 Flask 2.0）。虚拟环境为每个项目创建独立的 Python 环境，互不干扰。`source venv/bin/activate` 之后，你的终端就进入了这个隔离环境，退出用 `deactivate` 命令。
>
> **seed.py 做了什么？** 它会根据 `models.py` 中定义的结构，在数据库里自动创建对应的表（articles、categories、tags、users），并插入一些默认数据和一个管理员账号。

默认管理员：`admin` / `admin123`

### 4. 启动前端

```bash
cd frontend

# 安装前端依赖（Vue、Vite 等）
# node_modules 目录会很大，已在 .gitignore 中忽略，不提交到 git
npm install

# 启动开发服务器 http://localhost:3000
npm run dev
```

> **npm install 从哪里下载依赖？** 读取 `package.json` 中列出的依赖名称和版本，从 npm 官方仓库（registry.npmjs.org）下载到 `node_modules/` 目录。下载完成后会生成 `package-lock.json`，锁定每个包的精确版本，确保团队其他人安装时版本一致。

前端开发服务器会自动将 `/api` 请求代理到后端 `http://localhost:5000`。

### 5. 访问

| 地址 | 说明 |
|------|------|
| http://localhost:3000 | 博客前台（所有人可见） |
| http://localhost:3000/admin | 管理后台（需登录） |
| http://localhost:3000/admin/login | 管理员登录 |

## API 接口

> **什么是 API 接口？** API 是前后端之间通信的"合约"。前端按照约定的路径和方法发送请求，后端按照约定返回数据。下面列出的是本项目所有的接口。

### 公开接口

> 这些接口不需要登录就能访问，供博客读者使用。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/public/articles` | 文章列表（分页、分类、标签、关键词） |
| GET | `/api/public/articles/:id` | 文章详情（含阅读计数） |
| GET | `/api/public/articles/:id/nearby` | 上一篇/下一篇文章 |
| GET | `/api/public/categories` | 分类列表 |
| GET | `/api/public/tags` | 标签列表 |
| GET | `/api/public/about` | 关于信息 |

> **`:id` 是什么意思？** 路径中的 `:id` 是动态参数，实际请求时替换为具体数字。比如 `GET /api/public/articles/5` 获取 id 为 5 的文章。
>
> **GET 是什么意思？** HTTP 方法。GET（获取数据）、POST（创建数据）、PUT（更新数据）、DELETE（删除数据）。这是 RESTful API 的约定——用不同的 HTTP 方法对同一个路径做不同操作。

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 登录（提交用户名密码，返回 JWT 令牌） |
| POST | `/api/auth/register` | 注册新用户 |
| GET | `/api/auth/me` | 获取当前登录用户信息 |
| PUT | `/api/auth/me` | 更新个人信息 |

> **JWT 令牌是什么？** 用户登录成功后，后端返回一个加密的字符串（令牌）。前端把这个令牌保存在浏览器中，之后每次请求时附带在请求头里。后端验证令牌的有效性就知道"这个请求是谁发来的"，不需要每次请求都输入密码。令牌有过期时间（本项目设为 24 小时），过期后需要重新登录。

### 管理接口（需 JWT）

> 以下所有接口都需要登录后才能访问。请求时需要在请求头中附带 `Authorization: Bearer <令牌>`。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/articles` | 文章列表 / 创建新文章 |
| GET/PUT/DELETE | `/api/articles/:id` | 文章详情 / 更新文章 / 删除文章 |
| GET/POST | `/api/categories` | 分类列表 / 创建分类 |
| PUT/DELETE | `/api/categories/:id` | 更新分类 / 删除分类 |
| GET/POST | `/api/tags` | 标签列表 / 创建标签 |
| PUT/DELETE | `/api/tags/:id` | 更新标签 / 删除标签 |
| POST | `/api/files` | 上传文件（图片等） |
| GET | `/api/files/list` | 列出已上传的文件 |
| GET | `/api/files/:filename` | 获取已上传的文件 |

## 常见问题

**Q: 为什么启动后端时报错 "Can't connect to MySQL server"？**

A: MySQL 服务没有运行。执行 `sudo systemctl start mysqld` 启动后再试。

**Q: 为什么 `pip install` 提示 "externally-managed-environment"？**

A: 你的系统（如 Arch Linux）禁止直接在系统 Python 中安装包。需要创建虚拟环境：`python3 -m venv venv && source venv/bin/activate`，然后再执行 `pip install`。

**Q: npm install 速度很慢怎么办？**

A: 可以配置国内镜像源：`npm config set registry https://registry.npmmirror.com`（淘宝镜像）。

**Q: 如何修改默认端口？**

A: 修改 `frontend/vite.config.js` 中的 `server.port`（前端端口）和 `backend/run.py` 中的 `app.run(port=...)`（后端端口）。
