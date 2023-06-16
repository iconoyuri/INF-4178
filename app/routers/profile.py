from fastapi import APIRouter, Depends, Query
from app.schemas import ProfileEntry
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import List, Union

router = APIRouter(
    prefix='/profile', tags=["Profile"]
)


@router.post('/add', response_model=None)
def post_profile_info(profile_entry: ProfileEntry, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to add a set {key, value} to a user's profile. Example : {key: 'real_name', value: 'John Snow'}",
                )):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$addToSet': {'entries': {'key':profile_entry.key,'value':profile_entry.value}}})


@router.get('/self', response_model=List[ProfileEntry])
def get_profile_info(user_login=Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to get all the profile informations registered by the user",
                )):
    user = client['User'].find_one({'login': user_login})
    profile = client['Profile'].find_one({'owner':user['_id']})
    return profile['entries']


@router.delete('/self', response_model=None)
def delete_profile_info(profile_entry:ProfileEntry,user_login=Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to get all the profile informations registered by the user",
                )):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$pull': {'entries': {'key':profile_entry.key,'value':profile_entry.value}}})


@router.put('/self', response_model=None)
def update_profile_info(late_profile_entry:ProfileEntry, new_profile_entry:ProfileEntry,user_login=Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to get all the profile informations registered by the user",
                )):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$pull': {'entries': {'key':late_profile_entry.key,'value':late_profile_entry.value}}})
    client['Profile'].update_one({'owner':user['_id']},{'$addToSet': {'entries': {'key':new_profile_entry.key,'value':new_profile_entry.value}}})


@router.get('/other/{target_login}', response_model=List[ProfileEntry])
def get_someone_else_profile_info(target_login : str, user_login=Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to get all the profile informations of another user identified by his login given as request parameter",
                )):
    user = client['User'].find_one({'login': target_login})
    profile = client['Profile'].find_one({'owner':user['_id']})
    return profile['entries']


