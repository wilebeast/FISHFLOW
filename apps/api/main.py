from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.router import api_router
from infrastructure.config.settings import get_settings


settings = get_settings()

app = FastAPI(title=settings.api_title, version=settings.api_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"service": settings.api_title, "version": settings.api_version}
