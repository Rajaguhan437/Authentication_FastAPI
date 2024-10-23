from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database.database import get_db
from database.model import User
from database.schema import UserCreate, UserID, UserLogin
from auth.jwt_handler import encodeJWT, decodeJWT
from auth.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse
import base64, json, time
from datetime import datetime, timedelta

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


router = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

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
def read_users(
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
    db: Session = Depends(get_db)
):
    try:
        userDetail = db.query(User).filter(User.username == user.username, User.role == user.role).first()
        if userDetail:
            if userDetail.username == user.username and verify_password(user.password, userDetail.password) and userDetail.role == user.role:
                tokens = encodeJWT(user.username, user.password ,user.role)
                return {"status_code":200, **tokens}
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
    access_token: str,
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="No Access token")
    
    decoded_token = decodeJWT(access_token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid Access token")
    
    decoded_token["exp"] = time.time() - 60 * 20
    new_token = encodeJWT(decoded_token["username"], decoded_token["password"], decoded_token["role"], decoded_token["exp"], decoded_token["exp"])
    return {"status_code":200, "msg": "Logged Out Successfully", "new_token":new_token}  