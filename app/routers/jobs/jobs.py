from fastapi import APIRouter, Depends, HTTPException,status
from app.schemas import JobModel, JobUpdateModel, JobCreationModel
from app.classes import Job
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import Optional, List
from bson.objectid import ObjectId


router = APIRouter(
    prefix='/jobs', tags=["Jobs"]
)

from app.routers.jobs import application

router.include_router(application.router)


@router.post('/')
def publish_job(job: JobCreationModel, user_login = Depends(get_current_user)):
    if len(job.title) <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Job title can't be empty")
    _job = job.dict()
    _job['offerer'] = user_login
    _job['status'] = Job.statuses[0]
    _job['applicants'] = []
    client['Jobs'].insert_one(_job)


@router.get('/all', response_model=dict)
def get_posted_jobs(user_login = Depends(get_current_user)):
    active_jobs = [Job(str(job['_id']),job['offerer'],job['title'],job['description'],job['location'],job['skills'], job['status'], job['applicants']).__dict__ for job in client['Jobs'].find({'offerer':user_login, 'status': Job.statuses[0]})]
    terminated_jobs = [Job(str(job['_id']),job['offerer'],job['title'],job['description'],job['location'],job['skills'], job['status'], job['applicants']).__dict__ for job in client['Jobs'].find({'offerer':user_login, 'status': Job.statuses[1]})]
    return {"active_jobs":active_jobs,"terminated_jobs":terminated_jobs}


@router.get('/{id}', response_model=Optional[JobModel])
def get_specific_job(id:str,user_login = Depends(get_current_user)):
    return client['Jobs'].find_one({'_id':ObjectId(id)})


@router.delete('/{id}')
def delete_job(id:str,user_login = Depends(get_current_user)):
    client['Jobs'].delete_one({'_id':ObjectId(id)})


@router.put('/{id}')
def update_job(job: JobUpdateModel, id:str,user_login = Depends(get_current_user)):
    if len(job.title) <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Job title can't be empty")
    if job.status not in Job.statuses:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Job status must be in set {set(Job.statuses)}")
    client['Jobs'].update_one({'_id':ObjectId(id)}, {'$set':job.dict()})

