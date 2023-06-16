from pydantic import BaseModel, EmailStr
from typing import List, Optional

#-------------------------------------    AUTHENTICATION     -------------------------------

class UserRegistrationForm(BaseModel):
    login: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str


class Skill(BaseModel):
    name: str
    grade: Optional[str]
    numeric_value: Optional[str]


class DetailsModel(BaseModel):
    first_name:str
    last_name:str
    country:str
    language:str
    bio:str


class Profile(BaseModel):
    owner: str
    details:DetailsModel
    skills: List[Skill]


class Job(BaseModel):
    offerer:str
    title:str
    description:str
    profile:Profile
    # profile:List[dict]

class UserModel(BaseModel):
    id:str
    login:str
    email:str
    profile_id:str
