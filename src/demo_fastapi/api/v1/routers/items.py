from fastapi import APIRouter, Depends
from requests import Session

from demo_fastapi.api.deps import get_db
from demo_fastapi.crud import crud_item
from demo_fastapi.schemas import item

router = APIRouter()


@router.get("/items/", response_model=list[item.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud_item.get_items(db, skip=skip, limit=limit)
    print(items)
    return items


@router.post("/users/{user_id: int}/items/", response_model=item.Item)
def create_item_for_user(
    user_id: int, item: item.ItemCreate, db: Session = Depends(get_db)
):
    """
    对应: data, params, json, payload, form, files, body, query, headers, cookies, path
    """
    return crud_item.create_user_item(db=db, item=item, user_id=user_id)
