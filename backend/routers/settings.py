from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import StoreSetting
from ..schemas import (
    StoreSettingCreate,
    StoreSettingResponse,
    StoreSettingUpdate,
)


router = APIRouter(
    prefix="/api/settings",
    tags=["Configurações"],
)


# =========================================================
# BUSCAR CONFIGURAÇÕES — PÚBLICO
# =========================================================

@router.get(
    "/",
    response_model=StoreSettingResponse,
)
def get_settings(
    db: Session = Depends(get_db),
):
    settings = (
        db.query(StoreSetting)
        .order_by(StoreSetting.id.asc())
        .first()
    )

    if not settings:
        raise HTTPException(
            status_code=404,
            detail="Configurações da loja ainda não cadastradas.",
        )

    return settings


# =========================================================
# CRIAR CONFIGURAÇÕES — ADM
# =========================================================

@router.post(
    "/",
    response_model=StoreSettingResponse,
    status_code=201,
)
def create_settings(
    settings_data: StoreSettingCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    existing_settings = (
        db.query(StoreSetting)
        .first()
    )

    if existing_settings:
        raise HTTPException(
            status_code=409,
            detail="As configurações da loja já foram cadastradas.",
        )

    settings = StoreSetting(
        whatsapp=settings_data.whatsapp,
        instagram=settings_data.instagram,
        address=settings_data.address,
    )

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return settings


# =========================================================
# ATUALIZAR CONFIGURAÇÕES — ADM
# =========================================================

@router.put(
    "/",
    response_model=StoreSettingResponse,
)
def update_settings(
    settings_data: StoreSettingUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    settings = (
        db.query(StoreSetting)
        .order_by(StoreSetting.id.asc())
        .first()
    )

    if not settings:
        raise HTTPException(
            status_code=404,
            detail="Configurações da loja ainda não cadastradas.",
        )

    update_data = settings_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    return settings