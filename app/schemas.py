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

class ProfileEntry(BaseModel):
    key: str
    value: str



class User:
    def __init__(self,id, login, email, password,profile_id) -> None:
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.profile_id = profile_id

class Profile:
    def __init__(self, owner) -> None:
        self.owner = owner
        self.entries = []

    def add_entry(self,entry):
        self.entries.append(entry)

# class ProfileEntry:
#     def __init__(self, key:str,value:str) -> None:
#         self.key = key
#         self.value = value
