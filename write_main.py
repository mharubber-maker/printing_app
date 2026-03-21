import os

base = '/home/ghazal/printing_app'
files = {}

# ============================================================
files['main.py'] = """from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from config.database import get_db, engine, Base
from config.settings import settings
from domain.orders.repository import OrderRepository
from domain.orders.router import router as orders_router
import uvicorn

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(orders_router)


# ========== الصفحة الرئيسية ==========
@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    search:  str = "",
    status:  str = "",
    db:      Session = Depends(get_db),
):
    repo   = OrderRepository(db)
    orders = repo.get_all(search=search, status=status)
    stats  = repo.get_stats()

    return templates.TemplateResponse("pages/dashboard.html", {
        "request": request,
        "orders":  orders,
        "stats":   stats,
        "search":  search,
        "status":  status,
    })


# ========== الإحصائيات (HTMX) ==========
@app.get("/stats", response_class=HTMLResponse)
async def get_stats(
    request: Request,
    db:      Session = Depends(get_db),
):
    stats = OrderRepository(db).get_stats()
    return templates.TemplateResponse("partials/stats.html", {
        "request": request,
        "stats":   stats,
    })


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
"""

# ============================================================
files['Dockerfile'] = """FROM python:3.11-slim

WORKDIR /app

# نصب المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# مجلد الصور
RUN mkdir -p static/uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# ============================================================
files['docker-compose.yml'] = """version: '3.8'

services:

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB:       printing_db
      POSTGRES_USER:     printing_user
      POSTGRES_PASSWORD: printing_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U printing_user -d printing_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - uploads_data:/app/static/uploads
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
  uploads_data:
"""

# ============================================================
files['.env'] = """DATABASE_URL=postgresql://printing_user:printing_pass@postgres:5432/printing_db
REDIS_URL=redis://redis:6379
APP_NAME=بيت الطباعة والألوان
SECRET_KEY=change-this-in-production-please
DEBUG=True
UPLOAD_DIR=static/uploads
MAX_FILE_SIZE=5242880
"""

# ============================================================
files['.env.example'] = """DATABASE_URL=postgresql://user:password@localhost:5432/printing_db
REDIS_URL=redis://localhost:6379
APP_NAME=بيت الطباعة والألوان
SECRET_KEY=your-secret-key-here
DEBUG=False
UPLOAD_DIR=static/uploads
MAX_FILE_SIZE=5242880
"""

# ============================================================
files['static/uploads/.gitkeep'] = ""

# ============================================================
for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    print(f"✅ {lines:3d} سطر ← {path}")

print("\n🎉 main.py + Docker اتكتبوا بنجاح")
print("\nالخطوة الجاية:")
print("  docker-compose up --build")