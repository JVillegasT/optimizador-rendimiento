from fastapi import FastAPI
from app.api import productos
from app.db.session import engine
from app.models.producto import Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al arrancar (dev only; en prod usar migraciones Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Optimizador de Rendimiento API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(productos.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
