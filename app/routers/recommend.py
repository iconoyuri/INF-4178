from fastapi import APIRouter, Depends
from app.schemas import JobModel, UserModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from app.classes import Job, User, Profile, Skill
from typing import List, Optional

router = APIRouter(
    prefix='/recommendation', tags=["Recommendation"]
)


@router.get('/job/', response_model=List[JobModel])
def get_specific_job(user_login = Depends(get_current_user)):

    jobs = [Job(str(job['_id']),job['offerer'],job['title'],job['description'],job['location'],[Skill(skill['name'],skill['grade'],skill['numeric_value']) for skill in job['skills']], job['status'], job['applicants']) for job in client['Jobs'].find({'offerer':user_login, 'status': Job.statuses[0]})]
    # jobs_skills = [[skill.name for skill in job.skills] for job in jobs]
    # jobs_skills = [job.skills for job in jobs]

    profile = client['Profile'].find_one({'owner':user_login})
    profile = Profile(owner = profile['owner'], skills = [Skill(skill['name'],skill['grade'],skill['numeric_value']) for skill in profile['skills']])
    # profile_skills = [skill.name for skill in profile.skills]
    # profile_skills = profile.skills

    # sorted_jobs_skills = sorted(jobs_skills, key=lambda skills: len(intersection(flatten_skills(skills),flatten_skills(profile_skills))))
    sorted_jobs = sorted(jobs, key=lambda job: len(intersection(flatten_skills(job.skills),flatten_skills(profile.skills))))

    return sorted_jobs

def flatten_skills(skills:List[Skill]):
    return [skill.name for skill in skills]


def intersection(list1, list2) -> List:
    return list(set(list1) & set(list2))

# @router.get('/user/{text}', response_model=List[UserSearchModel])
# def search_job(text:str, user_login=Depends(get_current_user)):
#     users = [User(user['login']).__dict__ for user in client['User'].find({"login":{"$regex":text}}).limit(5)]
#     return users