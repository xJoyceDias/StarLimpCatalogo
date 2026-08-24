from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import Kit
from ..schemas import (
    KitCreate,
    KitResponse,
    KitUpdate,
)


router = APIRouter(
    prefix="/api/kits",
    tags=["Kits"],
)


# =========================================================
# LISTAR KITS — PÚBLICO
# =========================================================

@router.get(
    "/",
    response_model=list[KitResponse],
)
def list_kits(
    db: Session = Depends(get_db),
):
    return (
        db.query(Kit)
        .order_by(Kit.id.desc())
        .all()
    )


# =========================================================
# BUSCAR KIT — PÚBLICO
# =========================================================

@router.get(
    "/{kit_id}",
    response_model=KitResponse,
)
def get_kit(
    kit_id: int,
    db: Session = Depends(get_db),
):
    kit = (
        db.query(Kit)
        .filter(Kit.id == kit_id)
        .first()
    )

    if not kit:
        raise HTTPException(
            status_code=404,
            detail="Kit não encontrado.",
        )

    return kit


# =========================================================
# CRIAR KIT — ADM
# =========================================================

@router.post(
    "/",
    response_model=KitResponse,
    status_code=201,
)
def create_kit(
    kit_data: KitCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    kit = Kit(
        name=kit_data.name,
        description=kit_data.description,
        price=kit_data.price,
        image_url=kit_data.image_url,
        badge=kit_data.badge,
        active=kit_data.active,
    )

    db.add(kit)
    db.commit()
    db.refresh(kit)

    return kit


# =========================================================
# ATUALIZAR KIT — ADM
# =========================================================

@router.put(
    "/{kit_id}",
    response_model=KitResponse,
)
def update_kit(
    kit_id: int,
    kit_data: KitUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    kit = (
        db.query(Kit)
        .filter(Kit.id == kit_id)
        .first()
    )

    if not kit:
        raise HTTPException(
            status_code=404,
            detail="Kit não encontrado.",
        )

    update_data = kit_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(kit, field, value)

    db.commit()
    db.refresh(kit)

    return kit


# =========================================================
# EXCLUIR KIT — ADM
# =========================================================

@router.delete(
    "/{kit_id}"
)
def delete_kit(
    kit_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    kit = (
        db.query(Kit)
        .filter(Kit.id == kit_id)
        .first()
    )

    if not kit:
        raise HTTPException(
            status_code=404,
            detail="Kit não encontrado.",
        )

    db.delete(kit)
    db.commit()

    return {
        "message": "Kit excluído com sucesso."
    }