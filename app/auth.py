from jwt import encode, decode
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from schemas import Token
from models import User,get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "f83c4b9d217ae56c0e5a8f41b672e490"
ALGORITHM = "HS256"

async def create_jwt(user:User)->Token:
    access_token = encode({'id':user.id}, SECRET_KEY,algorithm=ALGORITHM)
    return Token(access_token=access_token)

async def verify_access_token(access_token:str)->int:
    try:
        user_data = decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return user_data['id']
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="bad token")

async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db))-> User:
    user_id = await verify_access_token(token)
    user = db.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=401, detail="user does not exist")


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)