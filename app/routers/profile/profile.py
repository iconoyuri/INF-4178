from fastapi import APIRouter, Depends
from app.schemas import Profile
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from app.routers.profile import skills
from app.routers.profile import user_details

router = APIRouter(
    prefix='/profile', tags=["Profile"]
)

router.include_router(skills.router)
router.include_router(user_details.router)

@router.get('/', response_model=Profile)
def get_profile(user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    profile = client['Profile'].find_one({'owner':user['_id']})
    return profile

@router.get('/{target_login}', response_model=Profile)
def get_profile(target_login:str, user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': target_login})
    profile = client['Profile'].find_one({'owner':user['_id']})
    return profile