# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.sql import func

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Define a relationship with QueryLog (one-to-many)
    queries = relationship("QueryLog", back_populates="user")

# QueryLog model
class QueryLog(Base):
    __tablename__ = 'query_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to users table
    question = Column(Text)
    answer = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

    # Define relationship with User
    user = relationship("User", back_populates="queries")
