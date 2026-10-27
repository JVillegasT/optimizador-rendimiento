# Optimizador de Rendimiento API

Proyecto de portafolio para demostrar optimización de consultas, métricas y CI/CD.

## Stack
- Python 3.11+ / FastAPI
- PostgreSQL + SQLAlchemy 2.0 (async)
- Redis (caché)
- GitHub Actions (CI/CD)
- pytest / ruff / mypy

## Fases
1. **Baseline** (anti-patrón intencional): N+1, índices faltantes, LIKE sin índice
2. **Índices + EXPLAIN ANALYZE**
3. **Arreglar N+1 con JOINs**
4. **Caché con Redis**
5. **CI/CD pipeline + benchmarks automatizados**

## Levantar en local
```bash
docker run -d --name pg-opt -e POSTGRES_DB=optimizador -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
cp .env.example .env  # editar si hace falta
uvicorn app.main:app --reload
