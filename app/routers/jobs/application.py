from fastapi import APIRouter, Depends, HTTPException, status
from app.classes import Application
from app.schemas import ApplicationModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from bson.objectid import ObjectId
from typing import List

router = APIRouter(
    prefix='/applications', tags=["Applications"]
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
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
    client['Jobs'].update_one({"_id":ObjectId(job_id)}, {'$pull': {'applications': {"applicant_login": user_login}}})


@router.delete('/{job_id}/{applicant_login}')
def delete_application_to_job(job_id:str, applicant_login:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
    if job['offerer'] == user_login:
        client['Jobs'].update_one({"_id":ObjectId(job_id), 'offerer': user_login}, {'$pull': {'applications': {"applicant_login": applicant_login}}})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only the owner of the job can delete an application")

@router.put('/{job_id}/{applicant_login}')
def accept_application_to_job(job_id:str, applicant_login:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
    if job['offerer'] == user_login:
        client['Jobs'].update_one({"_id":ObjectId(job_id), 'offerer': user_login}, {'$pull': {'applications': {"applicant_login": applicant_login}}})
        client['Jobs'].update_one({"_id":ObjectId(job_id), 'offerer': user_login}, {'$addToSet': {'workers': Application(applicant_login,job_id, job['title']).__dict__}})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only the owner of the job can accept an application")


@router.get('/{job_id}', response_model=List[ApplicationModel])
def get_job_applicants(job_id:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
    return job['applications']


@router.get('/', response_model=List[ApplicationModel])
def get_own_job_applications(user_login = Depends(get_current_user)):
    profile = client['Profile'].find_one({"owner":user_login})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant profile")
    return profile['applications']


