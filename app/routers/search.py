from fastapi import APIRouter, Depends, Query
from app.schemas import UserSearchOutput,GroupSearchOutput
from app.routers.authentication.oauth2 import get_current_user
from app.globals import main_graph
from py2neo_schemas.nodes import User, Group
from typing import List, Union

router = APIRouter(
    prefix='/search', tags=["Search"]
)

@router.get('/user/{target_user_login}', response_model=List[UserSearchOutput])
def search_user(target_user_login: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to search for a user whose the login starts by the string given as parameter",
                )):
    users = User.match(main_graph).where(f"_.login STARTS WITH '{target_user_login}'").limit(4)
    result = [UserSearchOutput(login=user.login) for user in list(users)]
    return result


@router.get('/group/{target_group}', response_model=List[GroupSearchOutput])
def search_group(target_group: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to search for a group whom the id or the name starts by the string given as parameter",
                )):
    groups = Group.match(main_graph).where(f"_.name STARTS WITH '{target_group}' OR _.identifier STARTS WITH '{target_group}'").limit(4)
    result = [GroupSearchOutput(identifier=group.identifier, name=group.name) for group in list(groups)]
    return result