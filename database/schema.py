from pydantic import BaseModel, Field, EmailStr
from database.enum import User_Role

# %% Define the Pydantic model
class UserCreate(BaseModel):
    username: str = Field(..., description="The username of the user", min_length=1, pattern="[^ ]+", example="username")
    email: EmailStr = Field(..., description="The email of the user", example="username@mail.com")
    password: str = Field(..., description="The password of the user", min_length=8, pattern="[^ ]+", example="zdr67ujko02ws")
    role: User_Role = Field(..., description="The role of the user")


class BookUpdate(BaseModel):
    name: str | None = Field(None, description="The name of the book", min_length=1, pattern="[^ ]+")
    author: str | None = Field(None, description="The author of the book", min_length=1, pattern="[^ ]+")
    price: float | None = Field(None, description="The price of the book", ge=0)


class UserLogin(BaseModel):
    username: str = Field(..., description="The username of the user", min_length=1, pattern="[^ ]+", example="username")
    password: str = Field(..., description="The password of the user", min_length=8, pattern="[^ ]+", example="zdr67ujko02ws")
    role: User_Role = Field(..., description="The role of the user")


class UserID(UserCreate):
    id: int 
