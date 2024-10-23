from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from database.database import get_db
from auth.jwt_bearer import JWTBearer
from database.schema import detailsInfo, categoryDetails, subCategoryDetails
from database.model import Details, Category, Sub_Category, User
from auth.jwt_handler import decodeJWT

router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/create/",
    description="Creating a New Category",
    dependencies=[Depends(JWTBearer())]
)
def Create_Category(
    category : categoryDetails ,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = request.headers.get("authorization")[7:]
        payload_dict = decodeJWT(token)

        username = payload_dict["username"]
        details = db.query(User).filter(User.username == username).first()

        categoryDict = {
            "cat_name" : category.cat_name,
            "created_by": details.id
            }
        categoryCreate = Category(**categoryDict) 
        
        db.add(categoryCreate)
        db.commit()
        db.refresh(categoryCreate)

        return {"status_code":200, **categoryDict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    
