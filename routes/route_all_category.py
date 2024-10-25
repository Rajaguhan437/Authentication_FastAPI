from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from database.database import get_db
from auth.jwt_bearer import JWTBearer
from database.schema import subCategoryDetails, allCategoryDetails, CategoryRead
from database.model import  Category, Sub_Category, User
from auth.jwt_handler import decodeJWT
from sqlalchemy import desc
from pprint import pprint
from routes.route_user import blacklist_token_check

router = APIRouter(
    prefix="/All-category",
    tags=["All-Category"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/create/",
    description="Creating New Category of Sub-Category",
    dependencies=[Depends(JWTBearer())]
)
def Create_subCategory(
    allcategory_list : list[allCategoryDetails] ,
    request: Request,
    db: Session = Depends(get_db),
):    
    try:
        token = request.headers.get("authorization")[7:]
        payload_dict = decodeJWT(token)

        username = payload_dict["username"]
        user_details = db.query(User).filter(User.username == username).first()

        cat_details = db.query(Category).order_by(desc(Category.cat_id)).first()
        id_no  = cat_details.cat_id

        for allcategory in allcategory_list:
            
            id_no += 1
            allcategoryDict_cat = {
                "cat_name": allcategory.cat_name,
                "created_by": user_details.id,
                "cat_id": id_no
            }
            categoryCreate = Category(**allcategoryDict_cat) 
            db.add(categoryCreate)
            
            for sub_cat_name in allcategory.sub_cat_list:

                allcategoryDict_subcat = {
                    "sub_cat_name" : sub_cat_name,
                    "created_by": user_details.id,
                    "cat_id": id_no
                    }
                subcategoryCreate = Sub_Category(**allcategoryDict_subcat) 
                db.add(subcategoryCreate)
        db.commit()
        return {"status_code":200, "msg":"Successfully Done"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        

@router.get(
    "/read/",
    description="Creating New Category of Sub-Category",
    dependencies=[Depends(JWTBearer())]
)
@blacklist_token_check
def read_allCategory(
    request: Request,
    db: Session = Depends(get_db),
):
    details_dict = {}
    try:
        categoryDetails_list = db.query(Category).all()
        for categoryDetails in categoryDetails_list:
            subCategoryDetails_list = db.query(Sub_Category).filter(Sub_Category.cat_id == categoryDetails.cat_id).all()
            temp = []
            for subCategoryDetails in subCategoryDetails_list:
                temp.append(subCategoryDetails.sub_cat_name)
            if temp:
                details_dict[categoryDetails.cat_name] = temp
        pprint(details_dict)
        return {**details_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))