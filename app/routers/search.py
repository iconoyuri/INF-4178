from fastapi import APIRouter, Depends
from app.schemas import JobSearchModel, UserSearchModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from app.classes import Job, User
from typing import List

router = APIRouter(
    prefix='/search', tags=["Search"]
)


@router.get('/job/{text}', response_model=List[JobSearchModel])
def search_job(text:str, user_login=Depends(get_current_user)):
    jobs = [Job(id=str(job['_id']),offerer=job['offerer'],title=job['title'],description=job['description'],location=job['location'],status=job['status']).__dict__ for job in client['Jobs'].find({"$and":[{"status":Job.statuses[0]},{"$or":[{"title":{"$regex":text}},{"description":{"$regex":text}}]}]})]
    return jobs


@router.get('/user/{text}', response_model=List[UserSearchModel])
def search_job(text:str, user_login=Depends(get_current_user)):
    users = [User(user['login']).__dict__ for user in client['User'].find({"login":{"$regex":text}}).limit(5)]
    return users