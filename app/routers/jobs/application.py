from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import DetailsModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter(
    prefix='/application', tags=["Application"]
)

@router.post('/new/{job_id}')
def apply_for_a_job(job_id:str, user_login = Depends(get_current_user)):
    client['Jobs'].update_one({"_id":ObjectId(job_id)}, {'$addToSet': {'applicants': {"user": user_login, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}}})


@router.delete('/{job_id}')
def delete_application_to_job(job_id:str, user_login = Depends(get_current_user)):
    client['Jobs'].update_one({"_id":ObjectId(job_id)}, {'$pull': {'applicants': {"user": user_login}}})


@router.delete('/{job_id}/{applicant_login}')
def delete_application_to_job(job_id:str, applicant_login:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if job['offerer'] == user_login:
        client['Jobs'].update_one({"_id":ObjectId(job_id), 'offerer': user_login}, {'$pull': {'applicants': {"user": applicant_login}}})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only the owner of the job can delete an application")


@router.get('/{job_id}/applicants')
def get_job_applicants(job_id:str, user_login = Depends(get_current_user)):
    return client['Jobs'].find_one({"_id":ObjectId(job_id)})['applicants']
    
