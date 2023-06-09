from fastapi import status,HTTPException, Depends, Request, APIRouter, Query
from app.schemas import UserRegistrationForm, UserLoginResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.routers.authentication.token_handler import create_access_token
from app.routers.authentication.account_activation_handler import AccountActivationHandler
from py2neo_schemas.nodes import User, Profile
from app.globals import main_graph ,encodeing, CHAT_SERVER_DOMAIN
from app.functions import encode_password
from email_validator import validate_email, EmailNotValidError
from passlib.context import CryptContext
import requests
from typing import Union
from app.functions import encode_content

router = APIRouter(
    prefix = "",
    tags = ["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED,response_model=None)
async def register(regist_form: UserRegistrationForm, request : Request, q: Union[str, None] = Query(
                default=None,
                description="This API serves to register a new user on the platform",
                )):
    if regist_form.password != regist_form.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, 
            detail="The password and the confirmation password don't match"
        )

    try:
        validate_email(regist_form.email)
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or not existing email"
        )

    login = regist_form.login.lower()
    email = regist_form.email.lower()
        
    user = save_user(login, email, regist_form.password)
    try:
        send_activation_mail(user, request)
        add_user_to_chat_server(login)
    except Exception as e:
        main_graph.delete(user)
        raise e
    

@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
    q: Union[str, None] = Query(
        default=None,
        title="User login",
        description="This API serves to log a user to the backend service, by providing to him a token that the user will use to accompany every single requests he will make later",
    )): 
    username = login_form.username.lower()
    
    user = find_user(username, login_form.password)
    if user:
        if user.activated: 
            access_token = create_access_token(
                data={"sub": user.login}
            )
            return UserLoginResponse(access_token=access_token, token_type="bearer")
        else: 
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="This user account isn't yet activated. Look for the activation link in your mail box"
            )
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The user doesn't exists"
        )

@router.get("/activate/{registration_code}", response_model=None)
async def activate(registration_code:str,q: Union[str, None] = Query(
                default=None,
                description="This API serves to activate an created account, depending on the activation code of the user (doesn't concern frontend team)",
                )
    ):    
    strd = None
    try:
        import base64
        strd = registration_code.encode(encodeing)
        strd = base64.b64decode(strd)
        strd = strd.decode(encodeing)
    except:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid activation link"
            )
    user = User.match(main_graph,strd).first()
    if user :
        user.activated = True
        main_graph.push(user)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Activation succeeded")
    else: 
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid activation link"
            )

def add_user_to_chat_server(user_login : str) :
    r = requests.post(f'{CHAT_SERVER_DOMAIN}/add-user', data={"login": user_login})

def find_user(login, password):
    user = User.match(main_graph).where(f"_.email = '{login}' OR _.login = '{login}'").first()
    if not user: 
        return False    

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    same_password = pwd_context.verify(password, user.password)
    if same_password:
        return user 
    else: 
        return None


def save_user(login, email, password):
    user = User.match(main_graph).where(f"_.login = '{login}' OR _.email = '{email}'").first()

    if user :
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="The user already exists"
        )
    else:
        hashed_password = encode_password(password)
        user = User(login=login, email=email, password = hashed_password, profile_img = None) 
        profile = Profile()
        user.profile.add(profile)
        main_graph.push(user)
    return user


def send_activation_mail(user,request):
    str_enc = encode_content(user.login)
    AccountActivationHandler.send_activation_mail(user,str_enc,request)
    
def send_update_address_mail(user,new_address,request):
    import base64

    strc = new_address
    str_enc = strc.encode(encodeing)
    str_enc = base64.b64encode(str_enc)
    str_enc = str_enc.decode(encodeing)

    AccountActivationHandler.send_update_address_mail(user,str_enc,new_address,request)
    
