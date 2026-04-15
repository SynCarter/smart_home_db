import requests
import time
import random

BASE_URL = "http://127.0.0.1:8000"

DEVICES = [
    {"name": "Living Room AC", "device_type": "thermostat"},
    {"name": "Kitchen Fridge", "device_type": "appliance"},
    {"name": "Main Door Lock", "device_type": "security"}
]

registered_device_ids = []

print("--- Smart Home IoT Simulator ---")
for dev in DEVICES:
    try:
        response = requests.post(f"{BASE_URL}/devices/", json=dev)
        if response.status_code == 200:
            device_id = response.json()["id"]
            registered_device_ids.append(device_id)
            print(f"Registered {dev['name']} with ID: {device_id}")
    except Exception:
        print("Server offline.")
        exit()

print("\nStarting stream... (Injecting anomalies occasionally)")
iteration = 0

try:
    while True:
        dev_id = random.choice(registered_device_ids)
        metrics = ["temperature", "power_draw"]
        metric = random.choice(metrics)
        
        # Inject Anomaly every 8 iterations
        iteration += 1
        is_spike = iteration % 8 == 0

        if metric == "temperature":
            value = round(random.uniform(30.0, 35.0) if is_spike else random.uniform(18.0, 26.0), 2)
        else:
            value = round(random.uniform(1300.0, 2000.0) if is_spike else random.uniform(50.0, 600.0), 2)

        payload = {"device_id": dev_id, "metric": metric, "value": value}
        requests.post(f"{BASE_URL}/telemetry/", json=payload)
        
        time.sleep(random.uniform(0.5, 2.0))

except KeyboardInterrupt:
    print("\nStopped.")