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
]
app = FastAPI(
    title=APP_NAME,
    description="This is the main server of the chat app",
    openapi_tags=tags_metadata)


from app.routers.authentication import authentication
from app.routers import profile
app.include_router(authentication.router)
app.include_router(profile.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)  
