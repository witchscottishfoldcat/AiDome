from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.item import Item, ItemCreate
from services.item_service import get_item, get_items, create_item

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    return create_item(db=db, item=item)

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of items."""
    items = get_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific item by ID."""
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return db_item