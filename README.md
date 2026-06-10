# Personal Blog

A minimal, responsive personal tech blog with Markdown editing, code highlighting, and math formula rendering.

**Stack:** Vue 3 + Flask + MySQL

## Features

- Markdown articles with syntax highlighting (highlight.js) and LaTeX math (KaTeX)
- Article browsing with pagination, category filter, and tag filter
- Full-text search across titles and content
- JWT-secured admin panel with article CRUD, category/tag management, and image upload
- Dark-themed, responsive design via Tailwind CSS

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8.x/9.x

### Backend

```bash
cd backend
cp .env.example .env          # edit with your DB credentials
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py                 # create tables + admin user (admin / admin123)
python run.py                  # http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                    # http://localhost:3000
```

The Vite dev server proxies `/api` requests to `localhost:5000`.

| URL | Description |
|-----|-------------|
| http://localhost:3000 | Blog frontend |
| http://localhost:3000/admin | Admin panel (login required) |

## Project Structure

```
├── backend/                  # Flask API
│   ├── app/
│   │   ├── __init__.py       # App factory
│   │   ├── config.py         # Configuration
│   │   ├── models.py         # SQLAlchemy models
│   │   └── routes/           # API blueprints
│   ├── seed.py               # DB init + admin user
│   ├── run.py                # Entry point
│   └── uploads/              # Uploaded files
└── frontend/                 # Vue 3 SPA
    ├── src/
    │   ├── api/              # Axios wrappers
    │   ├── stores/           # Pinia stores
    │   ├── router/           # Vue Router config
    │   ├── components/       # Reusable components
    │   └── views/            # Page components
    └── vite.config.js        # Vite + proxy config
```

## Documentation

See [guide.md](guide.md) for detailed developer documentation including API reference, database schema, and deployment.
