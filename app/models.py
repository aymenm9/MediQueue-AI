from sqlalchemy import create_engine, JSON, ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import datetime
engine = create_engine('sqlite:///db.sqlite3')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(String(30))
    last_name:Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    chemo_need: Mapped[float] = mapped_column(Float, nullable=True)
    radio_need: Mapped[float] = mapped_column(Float, nullable=True)
    chemo_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    radio_data: Mapped[dict] = mapped_column(JSON, nullable=True)


# ChemoSlot model
class ChemoSlot(Base):
    __tablename__ = "chemo_slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    drug_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dosage: Mapped[str] = mapped_column(String(100), nullable=False)
    duration: Mapped[str] = mapped_column(String(50), nullable=False)  # E.g., "2 hours"
    method: Mapped[str] = mapped_column(String(50), nullable=False)  # IV, pill...
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Scheduled, Done...
    scheduled_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

# RadioSlot model
class RadioSlot(Base):
    __tablename__ = "radio_slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    machine_type: Mapped[str] = mapped_column(String(255), nullable=False)
    radiation_dose: Mapped[float] = mapped_column(Float, nullable=False)  # Measured in Gy
    target_area: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[str] = mapped_column(String(50), nullable=False)  # E.g., "20 min"
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Scheduled, Done...
    scheduled_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

# Admin model
class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # Hash this!

async def create_db(engine):
    Base.metadata.create_all(engine)



async def get_db():
    conn = Session(engine)
    try:
        yield conn
    finally:
        conn.close()