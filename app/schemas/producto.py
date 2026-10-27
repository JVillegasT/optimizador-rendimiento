from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ProductoBase(BaseModel):
    sku: str
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int = 0
    categoria: str

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
