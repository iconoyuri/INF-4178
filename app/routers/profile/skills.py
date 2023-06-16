from fastapi import APIRouter, Depends, Query
from app.schemas import Skill
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import List

router = APIRouter(
    prefix='/skills', tags=["Skills"]
)


@router.post('/', response_model=None)
def add_skill(skill: Skill, user_login = Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$addToSet': {'skills': {'name':skill.name,'grade':skill.grade, 'numeric_value':skill.numeric_value}}})


@router.get('/', response_model=List[Skill])
def get_skills(user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    profile = client['Profile'].find_one({'owner':user['_id']})
    return profile['skills']


@router.delete('/', response_model=None)
def delete_skill(skill:Skill,user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$pull': {'skills': {'name':skill.name,'grade':skill.grade, 'numeric_value':skill.numeric_value}}})


@router.put('/', response_model=None)
def update_skill(prev_skills_set:Skill, new_skills_set:Skill,user_login=Depends(get_current_user)):
    user = client['User'].find_one({'login': user_login})
    client['Profile'].update_one({'owner':user['_id']},{'$pull': {'skills': prev_skills_set.dict()}})
    client['Profile'].update_one({'owner':user['_id']},{'$addToSet': {'skills': new_skills_set.dict()}})
    return new_skills_set



