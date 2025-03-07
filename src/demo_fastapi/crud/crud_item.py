from sqlalchemy.orm import Session

from demo_fastapi.models import Item
from demo_fastapi.schemas import ItemCreate


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item_a = Item(**item.model_dump(exclude_unset=True), owner_id=user_id)
    db_item = Item()
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    Item.owner_id = user_id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
