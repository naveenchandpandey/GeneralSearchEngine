from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    min_qty = Column(Integer, default=1)
    max_qty = Column(Integer, default=1)
    description = Column(String)
    available = Column(Boolean, default=True)
