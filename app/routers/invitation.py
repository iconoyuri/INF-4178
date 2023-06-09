from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.routers.authentication.oauth2 import get_current_user
from app.globals import main_graph
from py2neo_schemas.nodes import User
from app.functions import ensure_not_null_node
from app.schemas import UserSearchOutput
from typing import List, Union

router = APIRouter(
    prefix='/invitation', tags=["Invitation"]
)

@router.get('/list/recieved', response_model=List[UserSearchOutput])
def list_invtations(user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to list all the invitations recieved by the user, and that he didn't respond to",
                )):
    user = User.match(main_graph, user_login).first()
    result = [UserSearchOutput(login=user.login) for user in list(user.did_invite)]
    return result

@router.get('/list/sent', response_model=List[UserSearchOutput])
def list_invtations(user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api lists all the invitations the users had sent to other users. We get then the login of the invited people",
                )):
    user = User.match(main_graph, user_login).first()
    result = [UserSearchOutput(login=user.login) for user in list(user.invited)]
    return result

@router.get('/new/{target_user_login}', response_model=str)
def invite_user(target_user_login: str, user_login = Depends(get_current_user), q: Union[str, None] = Query(
                default=None,
                description="This api allows to invite a new user. It takes in parameter the login of that user",
                )):
    user = User.match(main_graph, user_login).first()
    target = User.match(main_graph, target_user_login).first()
    ensure_not_null_node(target)
    if user in list(target.invited):
        accept_invitation(target_user_login=target_user_login, user_login=user_login)
        return
    else:
        user.invited.add(target)
        main_graph.push(user)
    return f"{target.login} successfully invited"

@router.get('/accept/{target_user_login}', response_model=str)
def accept_invitation(target_user_login: str, user_login = Depends(get_current_user), q: Union[str, None] = Query(
                default=None,
                description="This api allows to accept the invitation of a user. It takes as parameter the identifier of that user",
                )):
    user = User.match(main_graph, user_login).first()
    target = User.match(main_graph, target_user_login).first()
    ensure_not_null_node(target)
    if user in list(target.invited):
        user.did_invite.remove(target)
        user.relatives.add(target)
        main_graph.push(user)
    else:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Specified resource not found"
            )
    return f"Accepted {target.login} invitation"


@router.delete('/decline/{target_user_login}', response_model=str)
def decline_invitation(target_user_login: str, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="This api allows to decline a recieved invitation. That one will be immediatly deleted",
                )):
    user = User.match(main_graph, user_login).first()
    target = User.match(main_graph, target_user_login).first()
    ensure_not_null_node(target)
    if user in list(target.invited):
        user.did_invite.remove(target)
        main_graph.push(user)
    else:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Specified resource not found"
            )
    return f"Declined {target.login} invitation"
