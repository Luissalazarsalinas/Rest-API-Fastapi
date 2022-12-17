## Create tables 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

# Post Table
class Post(Base):

    # Table name 
    __tablename__ = "posts"

    # Columns
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "TRUE", nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text("now()"), nullable = False)

    # Foreing key
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

    # relationship
    owner = relationship("User")

# User table
class User(Base):

    __tablename__ = "users"

    # Columns
    id = Column(Integer, primary_key = True, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text("now()"), nullable = False)


# Vote table
class Vote(Base):

    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key = True, nullable = False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key = True, nullable = False)
