# Real-Time Smart Home Telemetry Engine

A high-performance IoT backend designed to eliminate latency in high-frequency sensor environments. This system replaces traditional HTTP polling with a real-time WebSocket streaming architecture and Edge AI monitoring.

## 🔴 The Bottleneck
Standard IoT architectures often rely on request-response (HTTP) cycles, which create significant lag when tracking rapid sensor changes. In thermal monitoring, a 2-second delay in data logging can be the difference between a safe system and hardware damage.

## 🚀 The Solution: Real-Time Interception
This project re-architects the data pipeline to ensure millisecond latency and proactive safety:
* **WebSocket Integration:** Continuous duplex connection for instant telemetry streaming.
* **Edge AI Middleware:** A deterministic logic layer that intercepts data in-flight to flag anomalies (thermal spikes/surges) before they reach the persistent storage.
* **Optimized Storage:** Tailored for time-series data handling to ensure fast retrieval of historical trends.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Asynchronous Performance)
* **Communication:** WebSockets (Real-time duplex streaming)
* **Database:** SQLite (Optimized for edge-deployment performance)
* **ORM:** SQLAlchemy (Structured data integrity)
* **Validation:** Pydantic (Type-safe telemetry schemas)

## ⚙️ Installation & Setup
Ensure you have Python 3.8+ installed.

**1. Clone and Navigate:**
```bash
git clone [https://github.com/SynCarter/smart_home_db.git]
cd smart-home-db
```

**2. Environment Setup:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

## 🚀 Running the System
To start the FastAPI server with the WebSocket engine enabled:
```bash
python run.py
```
*The server will initialize the SQLite database automatically and start listening for telemetry on ws://localhost:8000/ws*

## 📈 Key Outcomes
* **Zero-Lag Monitoring:** Achieved real-time data visibility across all connected nodes.
* **Proactive Safety:** System flags "Thermal Anomalies" instantly, reducing risk of hardware failure.
* **Efficiency:** Drastically reduced network overhead compared to traditional polling methods.

---
*Developed as part of a product-focused architecture initiative to eliminate real-world engineering friction.*
