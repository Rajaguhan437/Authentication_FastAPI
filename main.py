from fastapi import FastAPI, Request, Cookie
from fastapi.staticfiles import StaticFiles
# from fastapi.routing import APIRoute
# from starlette.requests import Request

from routes import route_user, route_category, route_sub_category, route_all_category
from database.model import Base
from database.database import engine

from logger import logger
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return {"message": "Hello from FastAPI!"}

app.include_router(route_user.router)
app.include_router(route_category.router)
app.include_router(route_sub_category.router)
app.include_router(route_all_category.router)

@app.middleware('http')
async def logger_middleware(request: Request, call_next, cookie = Cookie(None)):

    print("Starting API...")
    start_time = time.time()
    
    log_dict = { 
        'url':request.url.path,
        'method':request.method,
    }
    logger.info(log_dict)

    response = await call_next(request)
    processing_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(processing_time)

    response.set_cookie(key="mycookie", value="000000000", max_age=3600, path="/", secure=False)
    
    return response
