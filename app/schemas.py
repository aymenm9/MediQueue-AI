from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

# Token model (unchanged)
class Token(BaseModel):
    access_token: str

# Base User model (unchanged)
class BaseUser(BaseModel):
    user_name: str
    model_config = {"from_attributes": True}

# User Input model (chemo_need and radio_need removed)
class UserInput(BaseUser):
    fullname: str
    password: str
    data: Dict = Field(default_factory=dict)  # JSON-like data, defaults to empty dict

# User Output model (chemo_need and radio_need kept here, AI-determined)
class UserOutput(BaseUser):
    id: int
    fullname: str
    chemo_need: Optional[float] = Field(default=None, ge=0, le=100)  # AI-determined
    radio_need: Optional[float] = Field(default=None, ge=0, le=100)  # AI-determined
    data: Dict

# Login model (unchanged)
class Login(BaseModel):
    user_name: str
    password: str

# MedicalStaff Base model (unchanged)
class BaseMedicalStaff(BaseModel):
    fullname: str
    role: str  # Doctor, Nurse, Tech...
    model_config = {"from_attributes": True}

# MedicalStaff Input model (unchanged)
class MedicalStaffInput(BaseMedicalStaff):
    assigned_room: Optional[str] = None
    materials_needed: Optional[Dict] = Field(default=None)  # JSON-like data

# MedicalStaff Output model (unchanged)
class MedicalStaffOutput(BaseMedicalStaff):
    id: int
    assigned_room: Optional[str] = None
    materials_needed: Optional[Dict] = None

# ChemoSlot Base model (unchanged)
class BaseChemoSlot(BaseModel):
    drug_name: str
    dosage: str
    infusion_time: str  # E.g., "2 hours"
    method: str  # IV, pill...
    status: str  # Scheduled, Done...
    scheduled_at: datetime
    model_config = {"from_attributes": True}

# ChemoSlot Input model (unchanged)
class ChemoSlotInput(BaseChemoSlot):
    patient_id: int
    doctor_id: int

# ChemoSlot Output model (unchanged)
class ChemoSlotOutput(BaseChemoSlot):
    id: int
    patient_id: int
    doctor_id: int

# RadioSlot Base model (unchanged)
class BaseRadioSlot(BaseModel):
    machine_type: str
    radiation_dose: float
    target_area: str
    duration: str  # E.g., "20 min"
    status: str  # Scheduled, Done...
    scheduled_at: datetime
    model_config = {"from_attributes": True}

# RadioSlot Input model (unchanged)
class RadioSlotInput(BaseRadioSlot):
    patient_id: int
    doctor_id: int

# RadioSlot Output model (unchanged)
class RadioSlotOutput(BaseRadioSlot):
    id: int
    patient_id: int
    doctor_id: int

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