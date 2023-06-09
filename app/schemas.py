from pydantic import BaseModel, EmailStr

#-------------------------------------    AUTHENTICATION     -------------------------------

class UserRegistrationForm(BaseModel):
    login: str
    email: EmailStr
    password: str
    confirm_password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str

class ProfileInfo(BaseModel):
    key: str
    value: str

class UserSearchOutput(BaseModel):
    login: str

class GroupSearchOutput(BaseModel):
    identifier: str
    name: str
    description: str