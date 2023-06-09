from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas import ProfileInfo
from app.routers.authentication.oauth2 import get_current_user
from app.globals import main_graph
from py2neo_schemas.nodes import User, Profile_info
from typing import List, Union

router = APIRouter(
    prefix='/profile', tags=["Profile"]
)

@router.post('/add', response_model=None)
def add_profile_info(infos: ProfileInfo, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to add a set {key, value} to a user's profile. Example : {key: 'real_name', value: 'John Snow'}",
                )):
    user = User.match(main_graph, user_login).first()
    user_profile = list(user.profile)[0]
    profile_info = Profile_info(key = infos.key, value = infos.value)
    user_profile.content.add(profile_info)
    main_graph.push(user_profile)

@router.get('/self', response_model=List[ProfileInfo])
def get_profile_info(user_login=Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to get all the profile informations registered by the user",
                )):
    user = User.match(main_graph, user_login).first()
    user_profile = list(user.profile)[0]
    profile_infos = []
    for profile_info in user_profile.content:
        profile_infos.append(ProfileInfo(key = profile_info.key, value = profile_info.value))
    return profile_infos

@router.get('/other/{target_login}', response_model=List[ProfileInfo])
def get_profile_info(target_login : str, user_login=Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to get all the profile informations of another user identified by his login given as request parameter",
                )):
    user = User.match(main_graph, target_login).first()
    if not user :
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Specified user not found"
            )
    user_profile = list(user.profile)[0]
    profile_infos = []
    for profile_info in user_profile.content:
        profile_infos.append(ProfileInfo(key = profile_info.key, value = profile_info.value))
    return profile_infos


