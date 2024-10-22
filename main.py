from fastapi import FastAPI

from routes import route_user

from database.model import Base
from database.database import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(route_user.router)


