from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserRegistrationForm(BaseModel):
    login: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str


class SkillModel(BaseModel):
    name: str
    grade: Optional[str]
    numeric_value: Optional[int] = 1


class DetailsModel(BaseModel):
    first_name:Optional[str] = ''
    last_name:Optional[str] = ''
    country:Optional[str] = ''
    language:Optional[str] = ''
    bio:Optional[str] = ''


class ProfileModel(BaseModel):
    owner: str
    details: DetailsModel
    skills: List[SkillModel]


class JobModel(BaseModel):
    id:str = ''
    offerer:str = ''
    title:str = ''
    description:str = ''
    location:str = ''
    skills: Optional[List[SkillModel]] = []
    status: str


class JobCreationModel(BaseModel):
    title:str = ''
    description:str = ''
    location:str = ''
    skills: Optional[List[SkillModel]] = []

    
class JobUpdateModel(BaseModel):
    title:str = ''
    description:str = ''
    location:str = ''
    skills: Optional[List[SkillModel]] = []
    

class UserModel(BaseModel):
    login:str
    email:str
    profile_id:str
