from typing import List

class User:
    def __init__(self, login, email, password, activated=False) -> None:
        self.login = login
        self.email = email
        self.password = password
        self.activated = activated

class Details:
    def __init__(self, first_name:str='', last_name:str='', country:str='', language:str='', bio:str='') -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.language = language
        self.bio = bio
        
class Profile:
    def __init__(self, owner: str) -> None:
        self.owner : str = owner
        self.details : dict = Details().__dict__
        self.skills : Skill = []

class Skill:
    def __init__(self, name='', grade='', numeric_value=1) -> None:
        self.name : str = name
        self.grade : str = grade
        self.numeric_value : int = numeric_value

class Job:
    statuses = ['Actif', 'Terminé']
    def __init__(self, id:str,offerer:str,title:str,description:str,location:str,skills:List[Skill], status:str, applicants:List) -> None:
        self.id:str = id
        self.offerer:str = offerer
        self.title:str = title
        self.description:str = description
        self.location:str = location
        self.skills:List[Skill] = skills
        self.status:str = status
        self.applicants:List = applicants
