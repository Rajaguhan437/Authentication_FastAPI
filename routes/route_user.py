from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, Body, Request, Cookie, Response, File, UploadFile, status
from sqlalchemy.orm import Session
from database.database import get_db
from database.model import User, BlackListed_Tokens
from database.schema import UserCreate, UserID, UserLogin
from auth.jwt_handler import encodeJWT, decodeJWT
from auth.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse
from functools import wraps
from typing import Callable
import pandas as pd
import aiofiles
from pprint import pprint
import io, json, time

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


router = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses={404: {"description": "Not found"}}, # need to check
)

def blacklist_token_check(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        request: Request,
        db: Session = Depends(get_db),
        *args, **kwargs
    ):
        token = request.headers.get("authorization")[7:]
        if not token:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        
        is_blacklisted = db.query(BlackListed_Tokens).filter(BlackListed_Tokens.token == token).first()
        
        if is_blacklisted:
            if is_blacklisted.token == token:
                raise HTTPException(status_code=403, detail="User logged out. Please log in again.")
        try:    
            return await func(request=request, db=db, *args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))
    return wrapper


@router.post(
        "/signup/",
        # response_model=UserCreate,
        summary="Registering new User",
        description="Register a new user to the database",
)
def Sign_Up(
    user : UserCreate, 
    db: Session = Depends(get_db)
):
    try:
        userDict = {
            "username" : user.username,
            "email" : user.email,
            "password" : get_hashed_password(user.password),
            "role" : user.role.value
            }
        userReg = User(**userDict) 
        db.add(userReg)
        db.commit()
        db.refresh(userReg)
        tokens = encodeJWT(userDict["email"], userDict["password"], userDict["role"])
        msg = {"status_code":200, **tokens}
        #msg.set_cookie(key="refresh_token", value=tokens["refresh_token"])
        return msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/details/",
    response_model=list[UserID],
    summary="Retrieve all Users",
    description="Get a list of all Users",
    dependencies=[Depends(JWTBearer())]
)
@blacklist_token_check
async def read_users(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        userDetails = db.query(User).offset(skip).limit(limit).all()
        return userDetails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post(
    "/login/",
    description="check the user exists or not",
)
def check_users(
    user: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        userDetail = db.query(User).filter(User.username == user.username, User.role == user.role).first()
        if userDetail:
            if userDetail.username == user.username and verify_password(user.password, userDetail.password) and userDetail.role == user.role:
                tokens = encodeJWT(user.username, user.password ,user.role)
                response.set_cookie(key="access_token", value=tokens['access_token'])
                response.set_cookie(key="refresh_token", value=tokens['refresh_token'])
                response.status_code=200
                return {"Response":response}
        else:   
            raise HTTPException(status_code=404, detail="Invalid Login Details")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
        "/refresh",
        description="Creating a access token with refresh token"
)
async def refresh_token(
    refresh_token: str , 
    db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    
    decoded_token = decodeJWT(refresh_token, type='refresh')
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # payload = decoded_token.split('.')[1] 
    # payload_dict = base64.b64decode(payload)
    payload_dict = decoded_token
    userDetail = db.query(User).filter(User.username == payload_dict['username'], User.role == payload_dict['role']).first()
    if not userDetail:
        raise HTTPException(status_code=401, detail="User does not exist")
    
    tokens = encodeJWT(userDetail.email, userDetail.password, userDetail.role)
    return {"status_code":200, **tokens} 


@router.post(
    "/logout",
    description="To logout the Users",
    dependencies=[Depends(JWTBearer())]
)
async def Logout_Users(
    request: Request,
    db: Session = Depends(get_db)
):
    access_token = request.headers.get("authorization")[7:]
    if not access_token:
        raise HTTPException(status_code=401, detail="No Access token")
    
    decoded_token = decodeJWT(access_token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid Access token")
    
    blacklistedToken = BlackListed_Tokens(token=access_token)
    db.add(blacklistedToken)
    db.commit()
    db.refresh(blacklistedToken)
    
    #decoded_token["exp"] = time.time() - 60 * 20
    #new_token = encodeJWT(decoded_token["username"], decoded_token["password"], decoded_token["role"], decoded_token["exp"], decoded_token["exp"])
    return {
        "status_code":200, 
        "msg": "Logged Out Successfully", 
        #"new_token":new_token
    }  


@router.post(
    "/upload_file/",
    description="To read a file"
)
async def upload_file_with_ROM(
    file: UploadFile = File(...)
):
    filename = file.filename
    if filename[-5:] == '.xlsx':
        
        async with aiofiles.open("/home/rajaguhan/Projects/Authentication_FastAPI/static/temp/"+filename ,'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write

        df = pd.read_excel("/home/rajaguhan/Projects/Authentication_FastAPI/static/temp/"+filename, index_col="S_No.")
        json_data = df.to_dict(orient='index')
        
        # pprint(json_data)
        return JSONResponse(content={
            "message": "Converted To JSON Successfully", 
            "data":json_data
        }, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=422, detail="Only Excel Files can be uploaded")


@router.post(
    "/upload_file_fast/",
    description="To read a file"
)
async def upload_file_without_ROM(
    file: UploadFile = File(...)
):
    filename = file.filename
    if filename[-5:] == '.xlsx':
        
        bio = io.BytesIO(await file.read()) 
        df = pd.read_excel(bio, index_col="S_No.")

        df["created_at_x"] = df["created_at_x"].apply(lambda x: x.isoformat())
        df["updated_at_x"] = df["updated_at_x"].apply(lambda x: x.isoformat())
        df["created_at_y"] = df["created_at_y"].apply(lambda x: x.isoformat())
        df["updated_at_y"] = df["updated_at_y"].apply(lambda x: x.isoformat())

        json_data = df.to_dict(orient='index')
        
        # pprint(json_data)
        return JSONResponse(content={
            "message": "Converted To JSON Successfully", 
            "data":json_data
        }, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=422, detail="Only Excel Files can be uploaded")
    