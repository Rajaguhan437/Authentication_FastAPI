# %%
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, )
# %%
