from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product
from ..schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


router = APIRouter(
    prefix="/api/products",
    tags=["Produtos"],
)


# =========================================================
# LISTAR PRODUTOS
# =========================================================

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .order_by(Product.id.desc())
        .all()
    )


# =========================================================
# BUSCAR PRODUTO
# =========================================================

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    return product


# =========================================================
# CRIAR PRODUTO
# =========================================================

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        image_url=product_data.image_url,
        badge=product_data.badge,
        active=product_data.active,
        category_id=product_data.category_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# =========================================================
# ATUALIZAR PRODUTO
# =========================================================

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


# =========================================================
# EXCLUIR PRODUTO
# =========================================================

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Produto excluído com sucesso."
    }