from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, func
from app.db.session import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=False)  # SIN índice a propósito
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(12, 2), nullable=False)
    stock = Column(Integer, default=0)
    categoria = Column(String(100), index=False)  # SIN índice a propósito
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
