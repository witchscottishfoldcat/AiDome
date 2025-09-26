from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, BaseMixin

class Item(Base, BaseMixin):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="items")
    
    def __repr__(self):
        return f"<Item(id={self.id}, title='{self.title}')>"

# Add relationship to User model
from models.user import User
User.items = relationship("Item", back_populates="owner")