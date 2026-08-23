from typing import Optional

from pydantic import BaseModel, ConfigDict


# =========================================================
# CATEGORIAS
# =========================================================

class CategoryBase(BaseModel):
    name: str
    slug: str
    active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# PRODUTOS
# =========================================================

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0
    image_url: Optional[str] = None
    badge: Optional[str] = None
    rating: Optional[float] = None
    review: Optional[int] = None
    active: bool = True
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    badge: Optional[str] = None
    rating: Optional[float] = None
    review: Optional[int] = None
    active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# ESSÊNCIAS
# =========================================================

class EssenceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0
    image_url: Optional[str] = None
    badge: Optional[str] = None
    active: bool = True


class EssenceCreate(EssenceBase):
    pass


class EssenceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    badge: Optional[str] = None
    active: Optional[bool] = None


class EssenceResponse(EssenceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# BASES
# =========================================================

class BaseProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0
    image_url: Optional[str] = None
    badge: Optional[str] = None
    active: bool = True


class BaseProductCreate(BaseProductBase):
    pass


class BaseProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    badge: Optional[str] = None
    active: Optional[bool] = None


class BaseProductResponse(BaseProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# KITS
# =========================================================

class KitBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0
    image_url: Optional[str] = None
    badge: Optional[str] = None
    active: bool = True


class KitCreate(KitBase):
    pass


class KitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    badge: Optional[str] = None
    active: Optional[bool] = None


class KitResponse(KitBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# CONFIGURAÇÕES DA LOJA
# =========================================================

class StoreSettingBase(BaseModel):
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    address: Optional[str] = None


class StoreSettingCreate(StoreSettingBase):
    pass


class StoreSettingUpdate(StoreSettingBase):
    pass


class StoreSettingResponse(StoreSettingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)