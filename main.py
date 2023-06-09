from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.globals import APP_NAME
from app.functions import encode_content

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations to register, login, activate a newly created account",
    },
    {
        "name": "Profile",
        "description": "Operations to get profile informations of a user",
    },
    # {
    #     "name": "Search",
    #     "description": "Operations to search for a group a user based on his identifiers",
    # },
    # {
    #     "name": "Circle",
    #     "description": "Operations to get the whole list of members of a circle and to look for some other member inside that list",
    # },
    # {
    #     "name": "Invitation",
    #     "description": "Operations to invite a user to join another one's, accept the invitation, decline it, have a view of all the recived and sent invitations",
    # },
    # {
    #     "name": "Microservices",
    #     "description": "Operations to communicate with other services (doesn't concern the frontend team)",
    # },
    # {
    #     "name": "Group",
    #     "description": "Operations to handle groups on the platform, be it creation, deletion, joining, etc",
    # },
]
app = FastAPI(
    title=APP_NAME,
    description="This is the main server of the chat app",
    openapi_tags=tags_metadata)


from app.routers.authentication import authentication
from app.routers import profile, search, circle, invitation, microservices, group
app.include_router(authentication.router)
app.include_router(profile.router)
# app.include_router(search.router)
# app.include_router(circle.router)
# app.include_router(invitation.router)
# app.include_router(group.router)
# app.include_router(microservices.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)  
