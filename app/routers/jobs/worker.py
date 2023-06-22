from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import ApplicationModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import List
from bson.objectid import ObjectId

router = APIRouter(
    prefix='/workers', tags=["Workers"]
)

@router.delete('/{job_id}/{worker_login}')
def delete_job_worker(job_id:str, worker_login:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
    
    if job['offerer'] == user_login:
        client['Jobs'].update_one({"_id":ObjectId(job_id), 'offerer': user_login}, {'$pull': {'workers': {"applicant_login": worker_login}}})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only the owner of the job can remove a worker")

@router.get('/{job_id}', response_model=List[ApplicationModel])
def get_job_workers(job_id:str, user_login = Depends(get_current_user)):
    job = client['Jobs'].find_one({"_id":ObjectId(job_id)})
    print(job)
    if job:
        return job['workers']
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
        
