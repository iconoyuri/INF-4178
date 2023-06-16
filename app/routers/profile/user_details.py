from fastapi import APIRouter, Depends
from app.schemas import DetailsModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client

router = APIRouter(
    prefix='/details', tags=["Details"]
)

@router.get('/', response_model=DetailsModel)
def get_details(user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    profile = client['Profile'].find_one({'owner':user['_id']})
    return profile['details']

@router.put('/', response_model=None)
def update_details(prev_details:DetailsModel, new_details:DetailsModel,user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$pull': {'details': prev_details.dict()}})
    client['Profile'].update_one({'owner':user['_id']},{'$addToSet': {'details': new_details.dict()}})
    return new_details
