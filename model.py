from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    age = Column(Integer)
    user = relationship("Posts", back_populates="owner")


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_archived = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="user")
