from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from .core.config import settings
from .api.v1.router import api_router
from starlette.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Budgeteer API",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json" if settings.api_env != "production" else None,
    docs_url="/api/v1/docs" if settings.api_env != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")
