from fastapi import FastAPI, Request
#from starlette.requests import Request

from routes import route_user, route_category, route_sub_category, route_all_category

from database.model import Base
from database.database import engine

from logger import logger
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware('http')
async def logger_middleware(request: Request, call_next):
    print("Starting API...")
    start_time = time.time()
    log_dict = { 
        'url':request.url.path,
        'method':request.method
    }
    logger.info(log_dict)

    response = await call_next(request)
    processing_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(processing_time)
    return response

app.include_router(route_user.router)
app.include_router(route_category.router)
app.include_router(route_sub_category.router)
app.include_router(route_all_category.router)

