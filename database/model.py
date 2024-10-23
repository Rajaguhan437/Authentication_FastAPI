# %% importing modules
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
from sqlalchemy.util.langhelpers import symbol
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from database.enum import User_Role

from datetime import datetime

# %% For making columns non updatable and raise attribute error when done
class NonUpdateableColumnError(AttributeError):
    def __init__(self, cls, column, old_value, new_value, message=None):
        self.cls = cls
        self.column = column
        self.old_value = old_value
        self.new_value = new_value

        if message is None:
            self.message = 'Cannot update column {} on model {} from {} to {}: column is non-updateable.'.format(
                column, cls, old_value, new_value)


def make_nonupdateable(col):
    @event.listens_for(col, 'set')
    def unupdateable_column_set_listener(target, value, old_value, initiator):
        if old_value != symbol('NEVER_SET') and old_value != symbol('NO_VALUE') and old_value != value:
            raise NonUpdateableColumnError(col.class_.__name__, col.name, old_value, value)
        
# %% Creation of Tables
Base = declarative_base()

 
class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing':True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(User_Role))


class Details(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now() ,onupdate=func.now())
    
    created_by = Column(Integer, ForeignKey("users.id"))

class Category(Details):
    __tablename__ = "category"
    __table_args__ = {'extend_existing':True}

    cat_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    cat_name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

class Sub_Category(Details):
    __tablename__ = "sub_category"
    __table_args__ = {'extend_existing':True}

    sub_cat_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    cat_id = Column(Integer, ForeignKey('category.cat_id'))
    sub_cat_name = Column(String)

