from typing import List

class User:
    def __init__(self, login:str="", email:str="", password:str="", activated=False) -> None:
        self.login:str = login
        self.email:str = email
        self.password:str = password
        self.activated:bool = activated

class Application:
    def __init__(self,applicant_login:str, job_id:str, job_title:str = "") -> None:
        self.job_id:str = job_id
        self.job_title:str = job_title
        self.applicant_login:str = applicant_login

class Details:
    def __init__(self, first_name:str='', last_name:str='', country:str='', language:str='', bio:str='') -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.language = language
        self.bio = bio

class Skill:
    def __init__(self, name='', grade='', numeric_value=1) -> None:
        self.name : str = name
        self.grade : str = grade
        self.numeric_value : int = numeric_value

class Profile:
    def __init__(self, owner: str, details:dict=Details().__dict__,skills:List[Skill] = [],applications: List[Application] = []) -> None:
        self.owner : str = owner
        self.details : dict = details
        self.skills : List[Skill] = skills
        self.applications: List[Application] = applications

class Job:
    statuses = ['Actif', 'Terminé']
    def __init__(self, id:str="",offerer:str="",title:str="",description:str="",location:str="",skills:List[Skill]=None, status:str="", applicants:List=None) -> None:
        self.id:str = id
        self.offerer:str = offerer
        self.title:str = title
        self.description:str = description
        self.location:str = location
        self.skills:List[Skill] = skills
        self.status:str = status
        self.applicants:List = applicants