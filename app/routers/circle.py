from fastapi import APIRouter, Depends, Query
from app.schemas import UserSearchOutput
from app.routers.authentication.oauth2 import get_current_user
from app.globals import main_graph
from py2neo_schemas.nodes import User
from typing import List, Union

router = APIRouter(
    prefix='/circle', tags=["Circle"]
)

@router.get('/list', response_model=List[UserSearchOutput])
def list_relatives(user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api takes the user's token and returns all the other users belonging to this one circle",
                )):
    users = User.match(main_graph, user_login).first()
    result = [UserSearchOutput(login=user.login) for user in list(users.relatives)]
    return result

@router.get('/search/{target_user_login}', response_model=List[UserSearchOutput])
def search_user(target_user_login: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to search for a specific user inside the circle",
                )):
    user = User.match(main_graph, user_login).first()
    result = [UserSearchOutput(login=user.login) for user in list(user.relatives) if user.activated and user.login.startswith(target_user_login)]
    return result

