import uvicorn
from fastapi import FastAPI, Depends,HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import select
from http_exception import *
from schemas import UserInput, UserOutput, Token,Login
from models import engine, create_db, get_db 
from models import User
from auth import get_password_hash,verify_password, create_jwt, get_current_user
from ai_util import genrate_rating_chemo, genrate_rating_radio
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database on startup
    await create_db(engine)
    yield
    # Disconnect from the database on shutdown
    engine.dispose()

app = FastAPI(lifespan=lifespan)


@app.get('/get_current_user',responses={**auth_exaption})
async def root(user:User = Depends(get_current_user)):
    return UserOutput.model_validate(user)



@app.post("/signup", responses={**singup_exaption})
async def signup(user:UserInput, db:Session = Depends(get_db) )->Token:
    new_user = User(first_name = user.first_name, last_name = user.last_name,email = user.email, password = get_password_hash(user.password),chemo_need = None, radio_need = None)
    db.add(new_user)
    db.commit()
    return await create_jwt(new_user)

@app.post('/login',responses={**login_exaption})
async def login(login_data:Login, db:Session = Depends(get_db))-> Token:
    user:User = db.execute(select(User).where(User.email == login_data.email)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail='user name does not exist')
    
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail='Incorrect password')
    
    return await create_jwt(user)   

@app.post('/add_chemo_data',responses={**auth_exaption})
async def add_chemo_data(data:dict , user:User = Depends(get_current_user),db:Session = Depends(get_db))->float:
    user.chemo_need= genrate_rating_chemo(user)

@app.post('/add_radio_data',responses={**auth_exaption})
async def add_radio_data(data:dict , user:User = Depends(get_current_user),db:Session = Depends(get_db))->float:
    user.chemo_need= genrate_rating_radio(user)