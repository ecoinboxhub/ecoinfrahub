from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from config.settings import settings
from utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load the LLM and embedding models at startup so the first chat query
    # does not pay the one-time model-loading penalty. Loading is guarded by the
    # engines' singletons and failures are non-fatal so the server always starts.
    try:
        from app.backend.engine import llm_engine
        llm_engine.load()
    except Exception as e:
        logger.error(f"Failed to pre-load LLM model: {e}")
    try:
        from app.backend.embeddings import embedding_engine
        embedding_engine.load()
    except Exception as e:
        logger.error(f"Failed to pre-load embedding model: {e}")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Offline African Infrastructure & Environmental AI Assistant",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


# Built frontend (production build output). Served at "/" so the UI loads
# directly from http://127.0.0.1:8432 without a separate dev server.
STATIC_DIR = settings.base_dir / "frontend" / "dist"
ASSETS_DIR = STATIC_DIR / "assets"

if ASSETS_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/")
async def index(request: Request):
    index_file = STATIC_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file))
    return JSONResponse(
        {
            "app": settings.app_name,
            "version": settings.version,
            "docs": "/docs",
            "frontend": f"http://{settings.api_host}:{settings.api_port}",
        }
    )