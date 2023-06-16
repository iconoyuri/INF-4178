from fastapi import APIRouter, Depends
from app.schemas import ProfileModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from app.routers.profile import skills
from app.routers.profile import details
from typing import Optional

router = APIRouter(
    prefix='/profile', tags=["Profile"]
)

router.include_router(skills.router)
router.include_router(details.router)

@router.get('/', response_model=Optional[ProfileModel])
def get_profile(user_login=Depends(get_current_user)):
    profile = client['Profile'].find_one({'owner':user_login})
    return profile

@router.get('/{target_login}', response_model=Optional[ProfileModel])
def get_profile(target_login:str, user_login=Depends(get_current_user)):
    profile = client['Profile'].find_one({'owner':target_login})
    return profile