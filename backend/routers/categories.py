from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category
from ..schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


router = APIRouter(
    prefix="/api/categories",
    tags=["Categorias"],
)


# =========================================================
# LISTAR CATEGORIAS
# =========================================================

@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return (
        db.query(Category)
        .order_by(Category.name.asc())
        .all()
    )


# =========================================================
# BUSCAR CATEGORIA
# =========================================================

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada.",
        )

    return category


# =========================================================
# CRIAR CATEGORIA
# =========================================================

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201,
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing_category = (
        db.query(Category)
        .filter(
            (Category.name == category_data.name)
            | (Category.slug == category_data.slug)
        )
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma categoria com esse nome ou slug.",
        )

    category = Category(
        name=category_data.name,
        slug=category_data.slug,
        active=category_data.active,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# =========================================================
# ATUALIZAR CATEGORIA
# =========================================================

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada.",
        )

    update_data = category_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data or "slug" in update_data:
        new_name = update_data.get(
            "name",
            category.name,
        )
        new_slug = update_data.get(
            "slug",
            category.slug,
        )

        duplicate = (
            db.query(Category)
            .filter(
                Category.id != category_id,
                (
                    (Category.name == new_name)
                    | (Category.slug == new_slug)
                ),
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Já existe outra categoria com esse nome ou slug.",
            )

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


# =========================================================
# EXCLUIR CATEGORIA
# =========================================================

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada.",
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Categoria excluída com sucesso."
    }