# Developer Guide

## Architecture

The system follows a **single-backend, SPA-frontend** architecture:

```
Browser (Vue 3 SPA)
    │
    ├── /api/* ──── Vite proxy (dev) / Nginx (prod) ──── Flask (port 5000)
    │                                                       │
    │                                                   MySQL 8.x
    │
    └── static assets (HTML/CSS/JS) served by Vite dev server or Nginx
```

- **Frontend**: Vue 3 SPA bundled by Vite. All `/api` requests are proxied to Flask during development.
- **Backend**: Flask app factory pattern with blueprints for route grouping. Stateless — authentication is handled via JWT tokens passed in the `Authorization` header.
- **Database**: MySQL accessed through SQLAlchemy ORM. Migrations managed by Flask-Migrate (Alembic).

### Authentication Flow

```
POST /api/auth/login { username, password }
    → validate credentials (Werkzeug check_password_hash)
    → return { access_token } (JWT, 24h expiry)

Subsequent requests:
    Authorization: Bearer <access_token>
    → @jwt_required() decorator validates token
    → get_jwt_identity() returns current user id
```

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend framework | Vue 3 (Composition API) | ^3.4 |
| Build tool | Vite | ^5.0 |
| State management | Pinia | ^2.1 |
| Routing | Vue Router | ^4.2 |
| CSS framework | Tailwind CSS | ^3.4 |
| HTTP client | Axios | ^1.6 |
| Markdown rendering | markdown-it | ^14.0 |
| Code highlighting | highlight.js | ^11.9 |
| Math rendering | KaTeX | ^0.16 |
| Backend framework | Flask | 3.0 |
| ORM | Flask-SQLAlchemy | 3.1 |
| Migrations | Flask-Migrate (Alembic) | 4.0 |
| Auth | Flask-JWT-Extended | 4.6 |
| CORS | Flask-CORS | 4.0 |
| Database driver | PyMySQL | 1.1 |
| Database | MySQL | 8.x/9.x |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── __init__.py          # create_app() factory
│   │   ├── config.py            # Config class (env vars, JWT, upload limits)
│   │   ├── models.py            # User, Article, Category, Tag + article_tags table
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── public.py        # GET /api/public/* (no auth)
│   │       ├── auth.py          # POST /api/auth/*
│   │       ├── articles.py      # CRUD /api/articles/*
│   │       ├── categories.py    # CRUD /api/categories/*
│   │       ├── tags.py          # CRUD /api/tags/*
│   │       └── files.py         # POST /api/files/*
│   ├── run.py                   # Entry point: app.run(debug=True, port=5000)
│   ├── seed.py                  # db.create_all() + default admin user
│   ├── uploads/                 # Uploaded file storage
│   ├── requirements.txt
│   ├── .env                     # Secrets (never committed)
│   └── .env.example             # Template for .env
└── frontend/
    ├── src/
    │   ├── main.js              # createApp, register plugins
    │   ├── App.vue              # Root component
    │   ├── api/                 # Axios instance + per-resource API modules
    │   ├── stores/              # Pinia stores (auth, etc.)
    │   ├── router/              # Route definitions + navigation guards
    │   ├── components/          # Shared UI components (Navbar, Pagination, etc.)
    │   └── views/               # Page-level components
    ├── public/                  # Static assets copied as-is
    ├── index.html               # Vite HTML entry point
    ├── vite.config.js           # Vite config (dev server port, proxy)
    ├── tailwind.config.js
    ├── postcss.config.js
    └── package.json
```

## Database Schema

### Tables

**users**
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, auto-increment |
| username | VARCHAR(80) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(256) | NOT NULL |
| nickname | VARCHAR(80) | |
| avatar | VARCHAR(256) | |
| created_at | DATETIME | |

**categories**
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK |
| name | VARCHAR(80) | UNIQUE, NOT NULL |
| slug | VARCHAR(80) | UNIQUE, NOT NULL |
| description | VARCHAR(256) | |
| created_at | DATETIME | |

**articles**
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK |
| title | VARCHAR(256) | NOT NULL |
| slug | VARCHAR(256) | UNIQUE, NOT NULL |
| summary | VARCHAR(512) | |
| content | TEXT | |
| cover_image | VARCHAR(256) | |
| status | VARCHAR(20) | draft / published / hidden |
| is_pinned | BOOLEAN | |
| view_count | INTEGER | |
| created_at | DATETIME | |
| updated_at | DATETIME | auto-update |
| category_id | INTEGER | FK → categories.id |

**tags**
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK |
| name | VARCHAR(80) | UNIQUE, NOT NULL |
| slug | VARCHAR(80) | UNIQUE, NOT NULL |
| created_at | DATETIME | |

**article_tags** (join table)
| Column | Type | Constraints |
|--------|------|-------------|
| article_id | INTEGER | PK, FK → articles.id |
| tag_id | INTEGER | PK, FK → tags.id |

### Relationships

- **Category → Articles**: one-to-many (`category.articles`, `article.category`)
- **Article ↔ Tags**: many-to-many via `article_tags` join table (`article.tags`, `tag.articles`)

### Key Design Decisions

- **Slug-based URLs**: Each article/category/tag has a `slug` field (unique, URL-safe identifier) separate from `id` — enables SEO-friendly URLs and human-readable sharing links.
- **`lazy="dynamic"` on Category.articles and Tag.articles**: Returns a query object instead of loading all related articles immediately. Use `.count()` for article counts without fetching full records. Use `.all()` explicitly when you need the data.
- **`lazy="joined"` on Article.tags**: Tags are always loaded with the article in a single JOIN query — avoids N+1 queries since tags are almost always needed when displaying an article.
- **Two serialization methods**: `Article.to_dict()` includes all fields for the admin panel; `Article.to_public_dict()` excludes sensitive/internal fields for public endpoints.
- **Passwords**: Hashed with Werkzeug `generate_password_hash` (default: scrypt). Never stored in plaintext.

## API Reference

### Public Endpoints (no auth)

**GET /api/public/articles**

Query parameters:

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| per_page | int | 10 | Items per page |
| category | string | — | Filter by category slug |
| tag | string | — | Filter by tag slug |
| keyword | string | — | Search in title and content |
| status | string | published | Article status filter |

Response:
```json
{
  "articles": [...],
  "total": 42,
  "pages": 5,
  "current_page": 1
}
```

**GET /api/public/articles/:id** — Returns full article object with `view_count` incremented on each request.

**GET /api/public/articles/:id/nearby** — Returns previous and next articles (by `created_at`) within the same publication status:
```json
{
  "prev": { "id": 4, "title": "...", "slug": "..." } | null,
  "next": { "id": 6, "title": "...", "slug": "..." } | null
}
```

**GET /api/public/categories** — Returns all categories with article counts.

**GET /api/public/tags** — Returns all tags with article counts.

**GET /api/public/about** — Returns the "about" configuration record.

### Auth Endpoints

**POST /api/auth/login**
```json
// Request
{ "username": "admin", "password": "admin123" }

// Response (200)
{ "access_token": "eyJ..." }

// Response (401)
{ "msg": "Invalid username or password" }
```

**POST /api/auth/register** — Create a new user. Requires username and password.

**GET /api/auth/me** — Returns the current user's profile. Requires JWT.

**PUT /api/auth/me** — Update nickname/avatar for the current user. Requires JWT.

### Admin Endpoints (require JWT)

All admin endpoints expect header: `Authorization: Bearer <token>`

**Articles** (`/api/articles`)
- `GET /api/articles` — List all articles (any status). Supports same query params as public list.
- `POST /api/articles` — Create article. Body: `{ title, slug, content, summary, cover_image, status, is_pinned, category_id, tag_ids: [...] }`
- `GET /api/articles/:id` — Get article by id.
- `PUT /api/articles/:id` — Update article. Partial updates supported.
- `DELETE /api/articles/:id` — Delete article.

**Categories** (`/api/categories`)
- `GET /api/categories` — List categories.
- `POST /api/categories` — Create: `{ name, slug, description }`
- `PUT /api/categories/:id` — Update category.
- `DELETE /api/categories/:id` — Delete category (fails if articles reference it).

**Tags** (`/api/tags`)
- `GET /api/tags` — List tags.
- `POST /api/tags` — Create: `{ name, slug }`
- `PUT /api/tags/:id` — Update tag.
- `DELETE /api/tags/:id` — Delete tag.

**Files** (`/api/files`)
- `POST /api/files` — Upload file. Body: `multipart/form-data` with field `file`. Returns filename.
- `GET /api/files/list` — List uploaded files.
- `GET /api/files/:filename` — Download/retrieve a file.

## Development

### Environment Variables

All backend configuration is read from `backend/.env`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| SECRET_KEY | No | dev fallback | Flask secret key for session signing |
| JWT_SECRET_KEY | No | dev fallback | Key for JWT signing/verification |
| DATABASE_URL | No | `mysql+pymysql://root:password@localhost:3306/blog_db` | SQLAlchemy connection string |

In production, **always set all three** to strong random values.

### Adding a New API Endpoint

1. Define the route in the appropriate blueprint under `backend/app/routes/`.
2. Use `@jwt_required()` decorator for authenticated routes.
3. Return JSON responses with `jsonify()`.
4. Add the corresponding Axios call in `frontend/src/api/`.

### Running Migrations

The `seed.py` script uses `db.create_all()` which is fine for development. For production schema changes, use Flask-Migrate:

```bash
cd backend
source venv/bin/activate
flask db init        # first time only — creates migrations/ directory
flask db migrate -m "Description of change"
flask db upgrade
```

### Code Patterns

**Backend routes** follow this structure:
- Blueprint grouping by resource (articles, categories, etc.)
- Route handlers call `Model.query.filter_by(...)` → return `jsonify(result)`
- Validation is inline in route handlers (no separate request schema layer)
- Error responses use `jsonify({"error": "message"})` with appropriate HTTP status codes

**Frontend** follows Vue 3 conventions:
- `<script setup>` syntax with Composition API
- Pinia stores for global state (auth token, current user)
- Vue Router with `meta: { requiresAuth: true }` for admin route guards
- Axios instance with request interceptor that attaches JWT token from Pinia store

### Debugging

- **Backend**: `run.py` sets `debug=True`, which enables Flask's interactive debugger and auto-reload. Errors return stack traces in the response.
- **Frontend**: Vue DevTools browser extension is recommended for inspecting component state, Pinia stores, and route changes.
- **API testing**: Use `curl` or an HTTP client (Postman, Insomnia, etc.) against `http://localhost:5000/api/`. The JWT token from `/api/auth/login` can be pasted into the `Authorization` header.

## Deployment

### Build

```bash
# Frontend
cd frontend
npm run build       # Output in dist/

# Backend — no build step; just ensure venv is set up
cd backend
pip install -r requirements.txt
```

### Production Architecture

```
Nginx (port 80/443)
├── /api/*          → proxy_pass to Flask (gunicorn on port 5000)
├── /uploads/*      → alias to backend/uploads/
└── /*              → serve frontend/dist/ (static files)
```

Run Flask with a production WSGI server:

```bash
cd backend
source venv/bin/activate
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
```

### Configuration Checklist

- [ ] Set strong `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`
- [ ] Set `DATABASE_URL` to production MySQL instance
- [ ] Change default admin password (`admin123`) immediately
- [ ] Set `debug=False` in `run.py` or use gunicorn (debug is always off in gunicorn)
- [ ] Configure HTTPS via Nginx + Let's Encrypt
- [ ] Set `MAX_CONTENT_LENGTH` in `config.py` if larger uploads are needed
- [ ] Set up regular database backups

## Troubleshooting

**"Can't connect to MySQL server"**
MySQL service is not running. `sudo systemctl start mysqld`

**"MySQL server has gone away"**
Connection timed out. Add `pool_pre_ping=True` to SQLAlchemy engine options in `config.py`, or increase MySQL `wait_timeout`.

**"externally-managed-environment" on pip install**
Your Linux distribution (Arch, Debian 12+) blocks system-wide pip installs. Use a virtual environment: `python3 -m venv venv && source venv/bin/activate`, then run `pip install`.

**npm install is slow**
Switch to a regional mirror: `npm config set registry https://registry.npmmirror.com`

**Port 3000 or 5000 already in use**
`lsof -i :3000` or `lsof -i :5000` to find the process, then `kill <PID>`. Or change the ports in `vite.config.js` and `run.py`.

**Vite proxy not forwarding API requests**
Check that the Flask backend is running on port 5000 and `vite.config.js` proxy target matches. Restart the Vite dev server after config changes.
