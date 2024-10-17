from pydantic import BaseModel, Field

# %% Define the Pydantic model
class BookCreate(BaseModel):
    name: str = Field(..., description="The name of the book", min_length=1, pattern="[^ ]+")
    author: str = Field(..., description="The author of the book", min_length=1, pattern="[^ ]+")
    price: float = Field(..., description="The price of the book", ge=0)

class BookUpdate(BaseModel):
    name: str | None = Field(None, description="The name of the book", min_length=1, pattern="[^ ]+")
    author: str | None = Field(None, description="The author of the book", min_length=1, pattern="[^ ]+")
    price: float | None = Field(None, description="The price of the book", ge=0)

class BookID(BookCreate):
    id: int 