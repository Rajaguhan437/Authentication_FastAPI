from pydantic import BaseModel, Field, EmailStr
from database.enum import User_Role
from datetime import datetime
from typing import List
# %% Define the Pydantic model
class UserCreate(BaseModel):
    username: str = Field(..., description="The username of the user", min_length=1, pattern="[^ ]+", example="username")
    email: EmailStr = Field(..., description="The email of the user", example="username@mail.com")
    password: str = Field(..., description="The password of the user", min_length=8, pattern="[^ ]+", example="zdr67ujko02ws")
    role: User_Role = Field(..., description="The role of the user")

class UserLogin(BaseModel):
    username: str = Field(..., description="The username of the user", min_length=1, pattern="[^ ]+", example="username")
    password: str = Field(..., description="The password of the user", min_length=8, pattern="[^ ]+", example="zdr67ujko02ws")
    role: User_Role = Field(..., description="The role of the user")

class UserID(UserCreate):
    id: int 

class detailsInfo(BaseModel):
    created_at: datetime = Field(datetime.now(), description="The time the category was Created")
    updated_at: datetime = Field(datetime.now(), description="The time the category was Created")
    created_by: str = Field(default=None, description="The user who created this", example="BoB")

class categoryDetails(BaseModel):
    cat_name: str = Field(..., description="The name of the Category", example="Non-Veg")
    # cat_id: int = Field(..., description="The ID of the Category", example="1")
    # is_active: bool = Field(default=True, description="Whether the category is active?", example=True)

class subCategoryDetails(BaseModel):
    #sub_cat_id: int = Field(..., description="The ID of the Sub-Category", example="1")
    #cat_id: int = Field(..., description="The ID of the Category", example="1")
    sub_cat_name: str = Field(..., description="The name of the Sub-Category", example="Chicken")

class allCategoryDetails(categoryDetails):
    sub_cat_list: List[str] 

class CategoryRead(BaseModel):
    cat_id: int = Field(..., description="The ID of the Category", example="1")
    cat_name: str = Field(..., description="The name of the Category", example="Non-Veg")
    