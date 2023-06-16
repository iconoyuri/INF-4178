
class User:
    def __init__(self,id, login, email, password,profile_id) -> None:
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.profile_id = profile_id

class Details:
    def __init__(self,first_name:str, last_name:str, country:str, language:str, bio:str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.language = language
        self.bio = bio
        
# class Profile:
#     def __init__(self, owner) -> None:
#         self.owner = owner
#         self.entries = []

#     def add_entry(self,entry):
#         self.entries.append(entry)