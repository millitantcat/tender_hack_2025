from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.routes import router
import os

# Создание экземпляра FastAPI с подробной документацией
app = FastAPI(
    title="TenderHack Assistant API",
    description=(
        "Интеллектуальный ассистент для обработки запросов по категориям Портала поставщиков."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Подключение маршрутов API
app.include_router(router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "web")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "web"))

@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def home(request: Request):
    """
    Главная страница веб-интерфейса.

    Возвращает HTML-шаблон с интерфейсом пользователя.

    - **request**: объект запроса FastAPI
    """
    return templates.TemplateResponse("index.html", {"request": request})
