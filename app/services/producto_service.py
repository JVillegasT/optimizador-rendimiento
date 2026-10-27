from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate
from typing import List
import random

class ProductoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear_producto(self, data: ProductoCreate) -> Producto:
        producto = Producto(**data.model_dump())
        self.db.add(producto)
        await self.db.commit()
        await self.db.refresh(producto)
        return producto

    async def crear_muchos_productos(self, cantidad: int = 50000) -> int:
        """Inserta masivo SIN bulk insert (lento a propósito)"""
        categorias = ["Electrónica", "Ropa", "Hogar", "Deportes", "Libros", "Juguetes"]
        for i in range(cantidad):
            producto = Producto(
                sku=f"SKU-{i:06d}",
                nombre=f"Producto {i}",
                descripcion=f"Descripción larga del producto {i} " * 3,
                precio=round(random.uniform(10, 2000), 2),
                stock=random.randint(0, 500),
                categoria=random.choice(categorias),
            )
            self.db.add(producto)
            # Commit cada 100 para no explotar memoria (pero sigue siendo lento)
            if i % 100 == 0:
                await self.db.commit()
        await self.db.commit()
        return cantidad

    # ANTI-PATRÓN N+1: busca productos y por cada uno hace query separada
    async def listar_con_detalle_lento(self, limit: int = 100) -> List[dict]:
        stmt = select(Producto).limit(limit)
        result = await self.db.execute(stmt)
        productos = result.scalars().all()

        salida = []
        for p in productos:
            # Simula N+1: query extra por cada producto
            stmt_extra = select(func.count(Producto.id)).where(Producto.categoria == p.categoria)
            total_categoria = (await self.db.execute(stmt_extra)).scalar()
            salida.append({
                "id": p.id,
                "sku": p.sku,
                "nombre": p.nombre,
                "precio": float(p.precio),
                "categoria": p.categoria,
                "total_en_categoria": total_categoria,  # Esto causa N+1
            })
        return salida

    # Consulta con LIKE %...% sin índice (full table scan)
    async def buscar_por_nombre_like(self, termino: str, limit: int = 50) -> List[Producto]:
        stmt = select(Producto).where(
            Producto.nombre.ilike(f"%{termino}%")
        ).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
