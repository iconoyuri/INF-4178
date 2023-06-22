from fastapi import APIRouter, Depends, HTTPException, status
from app.classes import Application
from app.schemas import ApplicationModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter(
    prefix='/applications', tags=["Application"]
)

@router.post('/new/{job_id}')
def apply_for_a_job(job_id:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')

    application = Application(user_login,job_id,job['title'])
    client['Jobs'].update_one({"_id":ObjectId(job_id)}, {'$addToSet': {'applications': application.__dict__}})
    client['Profile'].update_one({'owner':user_login}, {'$addToSet': {'applications': application.__dict__}})


@router.delete('/{job_id}')
def delete_application_to_job(job_id:str, user_login = Depends(get_current_user)):
    client['Jobs'].update_one({"_id":ObjectId(job_id)}, {'$pull': {'applications': {"user_login": user_login}}})


@router.delete('/{job_id}/{applicant_login}')
def delete_application_to_job(job_id:str, applicant_login:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if job['offerer'] == user_login:
        client['Jobs'].update_one({"_id":ObjectId(job_id), 'offerer': user_login}, {'$pull': {'applications': {"user_login": applicant_login}}})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only the owner of the job can delete an application")

@router.get('/{job_id}', response_model=ApplicationModel)
def get_job_applicants(job_id:str, user_login = Depends(get_current_user)):
    return client['Jobs'].find_one({"_id":ObjectId(job_id)})['applications']

@router.get('/all', response_model=ApplicationModel)
def get_job_applications(user_login = Depends(get_current_user)):
    return client['Profile'].find_one({"owner":user_login})['applications']
    

