import uvicorn
from fastapi import FastAPI, Depends,HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import select
from http_exception import *
from schemas import UserInput, UserOutput, Token,Login, BaseChemoSlot, BaseRadioSlot
from models import engine, create_db, get_db 
from models import User, ChemoSlot,RadioSlot
from auth import get_password_hash,verify_password, create_jwt, get_current_user
from ai_util import genrate_rating_chemo, genrate_rating_radio
from faker import Faker
import random
from datetime import datetime, timedelta
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
async def root(user:User = Depends(get_current_user))->UserOutput:
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
async def add_chemo_data(data:dict , user:User = Depends(get_current_user),db:Session = Depends(get_db))->list[BaseChemoSlot]:
    user.chemo_need= genrate_rating_chemo(user)
    slots = []
    for i in range(10):
        slot = ChemoSlot(
            patient_id=user.id,
            drug_name=random.choice(["Cisplatin", "Paclitaxel", "Doxorubicin", "Methotrexate"]),
            dosage=f"{random.randint(50, 500)} mg",
            duration=f"{random.randint(1, 5)} weeks",
            method=random.choice(["IV", "Oral", "Injection"]),
            status=random.choice(["Scheduled", "Ongoing", "Completed", "Cancelled"]),
            scheduled_at=datetime.now() + timedelta(days=random.randint(1, 30))
        )
        db.add(slot)
    db.commit()
    slots_s = db.execute(select(ChemoSlot).where(ChemoSlot.patient_id == user.id)).all()
    for slot in slots_s:
        slots.append(BaseChemoSlot.model_validate(slot[0]))
    return slots

@app.post('/add_radio_data',responses={**auth_exaption})
async def add_radio_data(data:dict , user:User = Depends(get_current_user),db:Session = Depends(get_db))->list[BaseRadioSlot]:
    user.chemo_need= genrate_rating_radio(user)
    slots = []
    for i in range(10):
        slot = RadioSlot(
        patient_id=user.id,
        machine_type=random.choice(["Linear Accelerator", "CyberKnife", "Gamma Knife"]),
        radiation_dose=round(random.uniform(1.0, 5.0), 2),  # Random dose in Gy
        target_area=random.choice(["Lung", "Brain", "Liver", "Breast"]),
        duration=random.choice(["10 min", "20 min", "30 min", "40 min"]),
        status=random.choice(["Scheduled", "Completed", "Cancelled"]),
        scheduled_at=datetime.now() + timedelta(days=random.randint(1, 30))
    )
        db.add(slot)
    db.commit()

    slots_s = db.execute(select(RadioSlot).where(RadioSlot.patient_id == user.id)).all()
    for slot in slots_s:
        slots.append(BaseRadioSlot.model_validate(slot[0]))
    return slots

@app.get('/get_chemo_data',responses={**auth_exaption})
async def add_chemo_data(user:User = Depends(get_current_user),db:Session = Depends(get_db))->list[BaseChemoSlot]:
    slots = []
    slots_s = db.execute(select(ChemoSlot).where(ChemoSlot.patient_id == user.id)).all()
    for slot in slots_s:
        slots.append(BaseChemoSlot.model_validate(slot[0]))
    return slots
@app.get('/get_radio_data',responses={**auth_exaption})
async def add_radio_data(user:User = Depends(get_current_user),db:Session = Depends(get_db))->list[BaseRadioSlot]:
    slots = []
    slots_s = db.execute(select(RadioSlot).where(RadioSlot.patient_id == user.id)).all()
    for slot in slots_s:
        slots.append(BaseRadioSlot.model_validate(slot[0]))
    return slots