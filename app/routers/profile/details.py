from fastapi import APIRouter, Depends
from app.schemas import DetailsModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import Optional

router = APIRouter(
    prefix='/details', tags=["Details"]
)

@router.get('/', response_model=Optional[DetailsModel])
def get_details(user_login=Depends(get_current_user)):
    profile = client['Profile'].find_one({'owner':user_login})
    return profile['details']

@router.put('/', response_model=None)
def update_details(details:DetailsModel,user_login=Depends(get_current_user)):
    client['Profile'].update_one({'owner':user_login},{'$set': {'details': details.dict()}})
    return details
