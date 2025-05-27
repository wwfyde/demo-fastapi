import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from requests import Session
from sqlalchemy.dialects.postgresql import Insert, insert
from starlette import status

from demo_fastapi.core.deps import get_db, verify_token
from demo_fastapi.crud import crud_item
from demo_fastapi.models import Item
from demo_fastapi.schemas import item

router = APIRouter()


@router.get("/items/", response_model=list[item.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    is_valid: Annotated[bool, Depends(verify_token)] = False,
):
    if not is_valid:
        logging.info("认证返回了False")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    items = crud_item.get_items(db, skip=skip, limit=limit)
    print(items)
    return items


@router.post("/users/{user_id}/items/", response_model=item.Item)
def create_item_for_user(
    user_id: Annotated[int, Path(regex=r"^[0-9]+$")],
    item: item.ItemCreate,
    db: Session = Depends(get_db),
):
    """
    对应: data, params, json, payload, form, files, body, query, headers, cookies, path
    """
    return crud_item.create_user_item(db=db, item=item, user_id=user_id)


@router.post("/items/{id:int}", response_model=item.ItemOut, summary="Create")
def create_item(
    *,
    id: Annotated[int, Path(regex=r"^[0-9]+$")],
    item: item.ItemUpsert,
    db: Session = Depends(get_db),
):
    return crud_item.upsert_item(db=db, item=item, id=id)


@router.put("/items/{id}/upsert", response_model=item.ItemOut, summary="Upsert")
def update_item(
    *,
    id: int,
    item: item.ItemUpsert,
    db: Session = Depends(get_db),
):
    insert_stmt: Insert = insert(Item).values(id=id, data="inserted value")
    do_update_stmt = insert_stmt.on_conflict_do_update(
        constraint="id", set_={"data": "updated value"}
    )
    db.execute()
    return crud_item.upsert_item(db=db, item=item, id=id)
