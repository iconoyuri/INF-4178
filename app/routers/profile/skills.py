from fastapi import APIRouter, Depends
from app.schemas import SkillModel
from app.routers.authentication.oauth2 import get_current_user
from app.globals import client
from typing import List, Optional

router = APIRouter(
    prefix='/skills', tags=["Skills"]
)


@router.post('/', response_model=None)
def add_skill(skill: SkillModel, user_login = Depends(get_current_user)):
    client['Profile'].update_one({'owner':user_login},{'$addToSet': {'skills': skill.dict()}})


@router.get('/', response_model=Optional[List[SkillModel]])
def get_skills(user_login=Depends(get_current_user)):
    profile = client['Profile'].find_one({'owner':user_login})
    return profile['skills']


@router.delete('/', response_model=None)
def delete_skill(skill:SkillModel,user_login=Depends(get_current_user)):
    client['Profile'].update_one({'owner':user_login},{'$pull': {'skills': {'name':skill.name,'grade':skill.grade, 'numeric_value':skill.numeric_value}}})


@router.put('/', response_model=None)
def update_skill(prev_skills_set:SkillModel, new_skills_set:SkillModel,user_login=Depends(get_current_user)):
    client['Profile'].update_one({'owner':user_login},{'$pull': {'skills': prev_skills_set.dict()}})
    client['Profile'].update_one({'owner':user_login},{'$addToSet': {'skills': new_skills_set.dict()}})
    return new_skills_set



