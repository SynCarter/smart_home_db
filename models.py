from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String, default="resident")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    device_type = Column(String)
    status = Column(String, default="online")
    logs = relationship("TelemetryLog", back_populates="device")

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    metric = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_anomaly = Column(Boolean, default=False) # NEW: AI/Edge tracking

    device = relationship("Device", back_populates="logs")