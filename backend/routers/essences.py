from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import Essence
from ..schemas import (
    EssenceCreate,
    EssenceResponse,
    EssenceUpdate,
)


router = APIRouter(
    prefix="/api/essences",
    tags=["Essências"],
)


# =========================================================
# LISTAR ESSÊNCIAS — PÚBLICO
# =========================================================

@router.get(
    "/",
    response_model=list[EssenceResponse],
)
def list_essences(
    db: Session = Depends(get_db),
):
    return (
        db.query(Essence)
        .order_by(Essence.id.desc())
        .all()
    )


# =========================================================
# BUSCAR ESSÊNCIA — PÚBLICO
# =========================================================

@router.get(
    "/{essence_id}",
    response_model=EssenceResponse,
)
def get_essence(
    essence_id: int,
    db: Session = Depends(get_db),
):
    essence = (
        db.query(Essence)
        .filter(Essence.id == essence_id)
        .first()
    )

    if not essence:
        raise HTTPException(
            status_code=404,
            detail="Essência não encontrada.",
        )

    return essence


# =========================================================
# CRIAR ESSÊNCIA — ADM
# =========================================================

@router.post(
    "/",
    response_model=EssenceResponse,
    status_code=201,
)
def create_essence(
    essence_data: EssenceCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    essence = Essence(
        name=essence_data.name,
        description=essence_data.description,
        price=essence_data.price,
        image_url=essence_data.image_url,
        badge=essence_data.badge,
        active=essence_data.active,
    )

    db.add(essence)
    db.commit()
    db.refresh(essence)

    return essence


# =========================================================
# ATUALIZAR ESSÊNCIA — ADM
# =========================================================

@router.put(
    "/{essence_id}",
    response_model=EssenceResponse,
)
def update_essence(
    essence_id: int,
    essence_data: EssenceUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    essence = (
        db.query(Essence)
        .filter(Essence.id == essence_id)
        .first()
    )

    if not essence:
        raise HTTPException(
            status_code=404,
            detail="Essência não encontrada.",
        )

    update_data = essence_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(essence, field, value)

    db.commit()
    db.refresh(essence)

    return essence


# =========================================================
# EXCLUIR ESSÊNCIA — ADM
# =========================================================

@router.delete(
    "/{essence_id}"
)
def delete_essence(
    essence_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    essence = (
        db.query(Essence)
        .filter(Essence.id == essence_id)
        .first()
    )

    if not essence:
        raise HTTPException(
            status_code=404,
            detail="Essência não encontrada.",
        )

    db.delete(essence)
    db.commit()

    return {
        "message": "Essência excluída com sucesso."
    }