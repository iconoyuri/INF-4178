from fastapi import APIRouter, Depends, Query
from app.schemas import Job
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import List, Union


router = APIRouter(
    prefix='/jobs', tags=["Jobs"]
)


@router.post('/add', response_model=None)
def post_job(job: Job, user_login = Depends(get_current_user),q: Union[str, None] = Query(
                default=None,
                description="A user creates a new job, which can attract workers",
                )):
    user = client['User'].find_one({'login': user_login})
    # return User('te','um','dd','dd')

