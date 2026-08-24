from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import BaseProduct
from ..schemas import (
    BaseProductCreate,
    BaseProductResponse,
    BaseProductUpdate,
)


router = APIRouter(
    prefix="/api/bases",
    tags=["Bases"],
)


# =========================================================
# LISTAR BASES — PÚBLICO
# =========================================================

@router.get(
    "/",
    response_model=list[BaseProductResponse],
)
def list_bases(
    db: Session = Depends(get_db),
):
    return (
        db.query(BaseProduct)
        .order_by(BaseProduct.id.desc())
        .all()
    )


# =========================================================
# BUSCAR BASE — PÚBLICO
# =========================================================

@router.get(
    "/{base_id}",
    response_model=BaseProductResponse,
)
def get_base(
    base_id: int,
    db: Session = Depends(get_db),
):
    base = (
        db.query(BaseProduct)
        .filter(BaseProduct.id == base_id)
        .first()
    )

    if not base:
        raise HTTPException(
            status_code=404,
            detail="Base não encontrada.",
        )

    return base


# =========================================================
# CRIAR BASE — ADM
# =========================================================

@router.post(
    "/",
    response_model=BaseProductResponse,
    status_code=201,
)
def create_base(
    base_data: BaseProductCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    base = BaseProduct(
        name=base_data.name,
        description=base_data.description,
        price=base_data.price,
        image_url=base_data.image_url,
        badge=base_data.badge,
        active=base_data.active,
    )

    db.add(base)
    db.commit()
    db.refresh(base)

    return base


# =========================================================
# ATUALIZAR BASE — ADM
# =========================================================

@router.put(
    "/{base_id}",
    response_model=BaseProductResponse,
)
def update_base(
    base_id: int,
    base_data: BaseProductUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    base = (
        db.query(BaseProduct)
        .filter(BaseProduct.id == base_id)
        .first()
    )

    if not base:
        raise HTTPException(
            status_code=404,
            detail="Base não encontrada.",
        )

    update_data = base_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(base, field, value)

    db.commit()
    db.refresh(base)

    return base


# =========================================================
# EXCLUIR BASE — ADM
# =========================================================

@router.delete(
    "/{base_id}"
)
def delete_base(
    base_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    base = (
        db.query(BaseProduct)
        .filter(BaseProduct.id == base_id)
        .first()
    )

    if not base:
        raise HTTPException(
            status_code=404,
            detail="Base não encontrada.",
        )

    db.delete(base)
    db.commit()

    return {
        "message": "Base excluída com sucesso."
    }