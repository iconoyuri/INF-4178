from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.globals import APP_NAME

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations to register, login, activate a newly created account",
    },
    {
        "name": "Details",
        "description": "CRUD operations various user details",
    },
    {
        "name": "Skills",
        "description": "CRUD operations for a user's skills",
    },
    {
        "name": "Profile",
        "description": "CRUD operations on user profile, (details as skills)",
    },
]
app = FastAPI(
    title=APP_NAME,
    description=f"Backend service for the {APP_NAME} application. Yoroshiku onegai shimasu",
    openapi_tags=tags_metadata)


from app.routers.authentication import authentication
from app.routers.jobs import jobs
from app.routers.profile import profile
from app.routers import search
from app.routers import recommend
app.include_router(authentication.router)
app.include_router(profile.router)
app.include_router(jobs.router)
app.include_router(search.router)
app.include_router(recommend.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)  
