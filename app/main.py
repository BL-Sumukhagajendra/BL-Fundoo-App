from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.auth_router import router as auth_router

app = FastAPI(
    title="Fundoo App",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(auth_router)