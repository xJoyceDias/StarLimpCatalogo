from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    active = Column(Boolean, nullable=False, default=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)
    badge = Column(String(100), nullable=True)
    rating = Column(Float, nullable=True)
    review = Column(Integer, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True,
    )

    category = relationship("Category")

class Essence(Base):
    __tablename__ = "essences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)
    badge = Column(String(100), nullable=True)
    active = Column(Boolean, nullable=False, default=True)


class BaseProduct(Base):
    __tablename__ = "bases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)
    badge = Column(String(100), nullable=True)
    active = Column(Boolean, nullable=False, default=True)


class Kit(Base):
    __tablename__ = "kits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)
    badge = Column(String(100), nullable=True)
    active = Column(Boolean, nullable=False, default=True)


class StoreSetting(Base):
    __tablename__ = "store_settings"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp = Column(String(30), nullable=True)
    instagram = Column(String(100), nullable=True)
    address = Column(String(500), nullable=True)