from fastapi import FastAPI
from app.core.config import get_settings
from app.api.endpoints import embedding, search

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(embedding.router, prefix="/api", tags=["Embedding"])
app.include_router(search.router, prefix="/api", tags=["Search"])