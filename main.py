from fastapi import FastAPI

from database.model import Base
from database.database import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

