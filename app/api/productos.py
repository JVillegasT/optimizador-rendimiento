from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoCreate, ProductoRead
from typing import List

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/", response_model=ProductoRead, status_code=201)
async def crear_producto(data: ProductoCreate, db: AsyncSession = Depends(get_db)):
    service = ProductoService(db)
    return await service.crear_producto(data)

@router.post("/seed", status_code=201)
async def seed_productos(cantidad: int = Query(1000, le=50000), db: AsyncSession = Depends(get_db)):
    service = ProductoService(db)
    total = await service.crear_muchos_productos(cantidad)
    return {"insertados": total}

@router.get("/lentos", response_model=List[dict])
async def listar_lentos(limit: int = Query(100, le=500), db: AsyncSession = Depends(get_db)):
    service = ProductoService(db)
    return await service.listar_con_detalle_lento(limit)

@router.get("/buscar")
async def buscar_like(q: str = Query(..., min_length=1), limit: int = Query(50, le=200), db: AsyncSession = Depends(get_db)):
    service = ProductoService(db)
    productos = await service.buscar_por_nombre_like(q, limit)
    return [{"id": p.id, "sku": p.sku, "nombre": p.nombre, "precio": float(p.precio)} for p in productos]
