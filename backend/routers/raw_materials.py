from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import Product
from ..schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


router = APIRouter(
    prefix="/api/raw-materials",
    tags=["Matérias-Primas"],
)


# =========================================================
# LISTAR MATÉRIAS-PRIMAS — PÚBLICO
# =========================================================

@router.get(
    "/",
    response_model=list[ProductResponse],
)
def list_raw_materials(
    db: Session = Depends(get_db),
):
    return (
        db.query(Product)
        .join(Product.category)
        .filter(
            Product.category.has(slug="materias-primas"),
            Product.active == True,
        )
        .order_by(Product.id.desc())
        .all()
    )


# =========================================================
# BUSCAR MATÉRIA-PRIMA — PÚBLICO
# =========================================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_raw_material(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.category.has(slug="materias-primas"),
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Matéria-prima não encontrada.",
        )

    return product


# =========================================================
# CRIAR MATÉRIA-PRIMA — ADM
# =========================================================

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
)
def create_raw_material(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        image_url=product_data.image_url,
        badge=product_data.badge,
        rating=product_data.rating,
        review=product_data.review,
        active=product_data.active,
        category_id=product_data.category_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# =========================================================
# ATUALIZAR MATÉRIA-PRIMA — ADM
# =========================================================

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_raw_material(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.category.has(slug="materias-primas"),
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Matéria-prima não encontrada.",
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
# EXCLUIR MATÉRIA-PRIMA — ADM
# =========================================================

@router.delete(
    "/{product_id}"
)
def delete_raw_material(
    product_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.category.has(slug="materias-primas"),
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Matéria-prima não encontrada.",
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Matéria-prima excluída com sucesso."
    }