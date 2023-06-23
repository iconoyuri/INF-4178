from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import JobModel, ProfileModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from app.classes import Job, Profile, Skill
from typing import List
from bson.objectid import ObjectId

router = APIRouter(
    prefix='/recommendation', tags=["Recommendation"]
)

@router.get('/job/', response_model=List[JobModel])
def get_recommended_jobs(user_login = Depends(get_current_user)):

    jobs = [Job(str(job['_id']),job['offerer'],job['title'],job['description'],job['location'],[Skill(skill['name'],skill['grade'],skill['numeric_value']) for skill in job['skills']], job['status'], job['applicants']) for job in client['Jobs'].find({'status': Job.statuses[0]})]
    profile = client['Profile'].find_one({'owner':user_login})
    profile = Profile(owner = profile['owner'], skills = [Skill(skill['name'],skill['grade'],skill['numeric_value']) for skill in profile['skills']])
    sorted_jobs = sorted(jobs, key=lambda job: len(intersection(flatten_skills(job.skills),flatten_skills(profile.skills))), reverse=True)

    sorted_jobs_dicts = [job.__dict__ for job in sorted_jobs]
    return sorted_jobs_dicts

def flatten_skills(skills:List[Skill]):
    return [skill.name for skill in skills]


def intersection(list1, list2) -> List:
    return list(set(list1) & set(list2))

@router.get('/user/{job_id}', response_model=List[ProfileModel])
def get_recommended_profiles(job_id:str, user_login=Depends(get_current_user)):
    job = client['Jobs'].find_one({'_id' : ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexistant job")
    
    job = Job(str(job['_id']),job['offerer'],job['title'],job['description'],job['location'],[Skill(skill['name'],skill['grade'],skill['numeric_value']) for skill in job['skills']], job['status'], job['applicants'])
    
    profiles = [Profile(owner = profile['owner'], skills = [Skill(skill['name'],skill['grade'],skill['numeric_value']) for skill in profile['skills']]) for profile in client['Profile'].find()]

    sorted_profiles = sorted(profiles, key=lambda profile: len(intersection(flatten_skills(job.skills),flatten_skills(profile.skills))), reverse=True)
    sorted_profiles_dict = [profile.__dict__ for profile in sorted_profiles]
    return sorted_profiles_dict