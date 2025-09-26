from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate

def get_item(db: Session, item_id: int):
    """Retrieve an item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of items."""
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate, owner_id: int = None):
    """Create a new item."""
    db_item = Item(**item.dict(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item