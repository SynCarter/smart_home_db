from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import json
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Home DB - Realtime & Edge AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- WebSocket Manager for Real-Time Streaming ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- Schemas ---
class DeviceCreate(BaseModel):
    name: str
    device_type: str

class TelemetryCreate(BaseModel):
    device_id: int
    metric: str
    value: float

# --- Routes ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/devices/")
def register_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = models.Device(name=device.name, device_type=device.device_type)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.post("/telemetry/")
async def log_telemetry(telemetry: TelemetryCreate, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == telemetry.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # --- EDGE INTELLIGENCE: Anomaly Detection ---
    is_anomaly = False
    if telemetry.metric == "power_draw" and telemetry.value > 1200:
        is_anomaly = True
    elif telemetry.metric == "temperature" and telemetry.value > 28.0:
        is_anomaly = True

    # Save to DB
    db_log = models.TelemetryLog(
        device_id=telemetry.device_id,
        metric=telemetry.metric,
        value=telemetry.value,
        is_anomaly=is_anomaly
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    # Broadcast instantly to frontend
    broadcast_data = {
        "device_id": db_log.device_id,
        "metric": db_log.metric,
        "value": db_log.value,
        "is_anomaly": db_log.is_anomaly,
        "timestamp": db_log.timestamp.isoformat()
    }
    await manager.broadcast(json.dumps(broadcast_data))

    return db_log
@app.get("/telemetry/recent")
def get_recent_telemetry(limit: int = 20, db: Session = Depends(get_db)):
    """Fetches historical data so the dashboard isn't empty on load."""
    logs = db.query(models.TelemetryLog).order_by(models.TelemetryLog.timestamp.desc()).limit(limit).all()
    # Return reversed so chronological order is maintained on charts
    return logs[::-1]