from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

# Token model (unchanged)
class Token(BaseModel):
    access_token: str

# Base User model (unchanged)
class BaseUser(BaseModel):
    email: str
    first_name:str
    last_name:str
    model_config = {"from_attributes": True}

# User Input model (chemo_need and radio_need removed)
class UserInput(BaseUser):
    password: str
    data: Dict = Field(default_factory=dict)  # JSON-like data, defaults to empty dict

# User Output model (chemo_need and radio_need kept here, AI-determined)
class UserOutput(BaseUser):
    id: int
    chemo_need: Optional[float] = Field(default=None, ge=0, le=100)  # AI-determined
    radio_need: Optional[float] = Field(default=None, ge=0, le=100)  # AI-determined
    chemo_data: Dict
    radio_data: Dict

# Login model (unchanged)
class Login(BaseModel):
    email: str
    password: str



# ChemoSlot Base model (unchanged)
class BaseChemoSlot(BaseModel):
    id: int
    patient_id: int
    drug_name: str
    dosage: str
    duration: str
    infusion_time: str  # E.g., "2 hours"
    method: str  # IV, pill...
    status: str  # Scheduled, Done...
    scheduled_at: datetime
    model_config = {"from_attributes": True}


# RadioSlot Base model (unchanged)
class BaseRadioSlot(BaseModel):
    id: int
    patient_id: int
    machine_type: str
    radiation_dose: float
    target_area: str
    duration: str  # E.g., "20 min"
    status: str  # Scheduled, Done...
    scheduled_at: datetime
    model_config = {"from_attributes": True}


# Admin Base model (unchanged)
class BaseAdmin(BaseModel):
    fullname: str
    username: str
    model_config = {"from_attributes": True}

# Admin Input model (unchanged)
class AdminInput(BaseAdmin):
    password: str

# Admin Output model (unchanged)
class AdminOutput(BaseAdmin):
    id: int