from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from database.database import get_db
from auth.jwt_bearer import JWTBearer
from database.schema import subCategoryDetails
from database.model import  Category, Sub_Category, User
from auth.jwt_handler import decodeJWT

router = APIRouter(
    prefix="/sub-category",
    tags=["Sub-Category"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/create/",
    description="Creating a New Sub-Category",
    dependencies=[Depends(JWTBearer())]
)
def Create_subCategory(
    subcategory : subCategoryDetails ,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = request.headers.get("authorization")[7:]
        payload_dict = decodeJWT(token)

        username = payload_dict["username"]
        user_details = db.query(User).filter(User.username == username).first()
        cat_details = db.query(Category).filter(Category.created_by == user_details.id).first()

        subcategoryDict = {
            "sub_cat_name" : subcategory.sub_cat_name,
            "created_by": user_details.id,
            "cat_id": cat_details.cat_id,
            #"sub_cat_id": 2
            }
        subcategoryCreate = Sub_Category(**subcategoryDict) 
        
        db.add(subcategoryCreate)
        db.commit()
        db.refresh(subcategoryCreate)

        return {"status_code":200, **subcategoryDict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

