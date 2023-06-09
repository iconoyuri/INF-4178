
from fastapi import HTTPException, status
from app.globals import encodeing 

def encode_password(password) -> str:
    from passlib.context import CryptContext    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password

def ensure_not_null_node(node):
    if not node :
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Specified resource not found"
            )

def encode_content(content):
    import base64
    strc = content
    str_enc = strc.encode(encodeing)
    str_enc = base64.b64encode(str_enc)
    str_enc = str_enc.decode(encodeing)
    return str_enc

