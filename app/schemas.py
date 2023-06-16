from pydantic import BaseModel, EmailStr
from typing import List

#-------------------------------------    AUTHENTICATION     -------------------------------

class UserRegistrationForm(BaseModel):
    login: str
    email: EmailStr
    password: str
    confirm_password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    
#-------------------------------------    ENTITIES     -------------------------------



class User(BaseModel):
    id:str
    login:str
    email:str
    profile_id:str

class Profile(BaseModel):
    owner:str
    entries:List[dict]

class ProfileEntry(BaseModel):
    key: str
    value: str

