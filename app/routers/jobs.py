from fastapi import APIRouter, Depends, HTTPException,status
from app.schemas import JobModel
from app.classes import Job
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import Optional, List
from bson.objectid import ObjectId


router = APIRouter(
    prefix='/jobs', tags=["Jobs"]
)


@router.post('/', response_model=None)
def publish_job(job: JobModel, user_login = Depends(get_current_user)):
    if len(job.title) <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Job title can't be empty")
    job.offerer = user_login
    client['Jobs'].insert_one(job.dict())


@router.get('/all', response_model=Optional[List[JobModel]])
def get_posted_jobs(user_login = Depends(get_current_user)):
    jobs = [Job(str(job['_id']),job['offerer'],job['title'],job['description'],job['location'],job['skills']).__dict__ for job in client['Jobs'].find({'offerer':user_login})]
    return jobs


@router.get('/{id}', response_model=Optional[JobModel])
def get_specific_job(id:str,user_login = Depends(get_current_user)):
    return client['Jobs'].find_one({'_id':ObjectId(id)})


@router.delete('/{id}', response_model=Optional[JobModel])
def delete_job(id:str,user_login = Depends(get_current_user)):
    return client['Jobs'].delete_one({'_id':ObjectId(id)})


@router.put('/{id}', response_model=Optional[JobModel])
def update_job(job: JobModel, id:str,user_login = Depends(get_current_user)):
    if len(job.title) <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Job title can't be empty")
    client['Jobs'].insert_one(job.dict())
    return client['Jobs'].update_one({'_id':ObjectId(id)}, {'$set':job.dict().pop('id')})

