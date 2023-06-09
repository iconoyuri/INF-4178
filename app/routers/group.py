from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.schemas import GroupSearchOutput, UserSearchOutput
import requests
from app.routers.authentication.oauth2 import get_current_user
from app.globals import main_graph, CHAT_SERVER_DOMAIN
from py2neo_schemas.nodes import User, Group
from typing import List, Union
import time
from app.functions import encode_content

router = APIRouter(
    prefix='/group', tags=["Group"]
)


@router.get('/create/{group_name}', response_model=str)
def create_group(group_name: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to create a new group, passing in parameter only that group name",
                )):
    user = User.match(main_graph, user_login).first()
    identifier = encode_content(f"{time.time()}")
    group = Group(name=group_name, identifier=identifier, description="")
    add_group_to_chat_server(identifier)
    group.creator.add(user)
    group.members.add(user)
    main_graph.push(group)
    return "Group Successfully created"


@router.get('/all', response_model=List[GroupSearchOutput])
def list_groups(user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to list all the groups a user belongs to",
                )):
    user = User.match(main_graph, user_login).first()
    return [GroupSearchOutput(identifier=group.identifier, name=group.name, description=group.description) for group in list(user.groups)]


@router.get('/member/add/{group_id}/{friend_id}', response_model=str)
def add_friend_to_group(group_id: str, friend_id:str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to add a user to add another one of his circle to a group",
                )):
    user = User.match(main_graph, user_login).first()
    friend = User.match(main_graph, friend_id).first()
    group = Group.match(main_graph, group_id).first()
    if not friend or not group: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="friend or group not found")
    if not user in list(group.members):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not member of this group")
    group.members.add(friend)
    main_graph.push(group)
    return ""

@router.get('/list/{group_id}', response_model=List[UserSearchOutput])
def list_group_members(group_id: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to list all the members of a group",
                )):
    group = Group.match(main_graph, group_id).first()
    return [UserSearchOutput(login=user.login) for user in list(group.members)]

@router.delete('/member/eject/{target_user_login}/{group_id}', response_model=str)
def remove_member(target_user_login: str, group_id: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to delete a group. Only that group's creator can perform it",
                )):
    user = User.match(main_graph, user_login).first()
    target = User.match(main_graph, target_user_login).first()
    group = Group.match(main_graph, group_id).first()
    if not group: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if user in list(group.members):
        group.members.remove(target)
        main_graph.push(group)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="User fired")
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You cannot eject this user")
        
@router.delete('/group/{group_id}', response_model=str)
def delete_group(group_id: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to delete a group. Only that group's creator can perform it",
                )):
    user = User.match(main_graph, user_login).first()
    group = Group.match(main_graph, group_id).first()
    if not group: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if user in list(group.creator):
        main_graph.delete(group)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Group deleted")
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You cannot delete this group")
        



def add_group_to_chat_server(identifier : str) :
    r = requests.post(f'{CHAT_SERVER_DOMAIN}/add-group', data={"identifier": identifier})
