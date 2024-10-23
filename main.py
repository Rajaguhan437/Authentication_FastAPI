from fastapi import FastAPI

from routes import route_user, route_category, route_sub_category, route_all_category

from database.model import Base
from database.database import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(route_user.router)
app.include_router(route_category.router)
app.include_router(route_sub_category.router)
app.include_router(route_all_category.router)

