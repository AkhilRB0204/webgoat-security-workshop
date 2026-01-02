# backend/app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from freight_trading import FreightSim
import threading
import time
import os

app = FastAPI()

# Allow cross-origin requests so frontend can fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sim = None  # Global simulation instance
sim_lock = threading.Lock() # Lock for thread-safe simulation access

# Background thread to continuously update truck positions and reassign loads
def run_sim():
    while True:
        if sim:
            sim.assign_loads()   # Dynamically assign loads
            sim.update_trucks()  # Move trucks step by step
        time.sleep(1)  # Update every second

# Start the background simulation thread
threading.Thread(target=run_sim, daemon=True).start()

# --- Initialize simulation ---
@app.get("/init")
def init_sim(
    num_trucks: int = Query(50, description="Number of trucks"),
    num_loads: int = Query(20, description="Number of loads"),
    min_pop: int = Query(100000, description="Minimum city population"),
    enable_finance: bool = Query(False, description="Enable finance tracking")
):
    global sim

    # csv path for city data
    csv_path = os.path.join(os.path.dirname(__file__), "uscities.csv")
    # Create new FreightSim instance with finance tracking option
    sim = FreightSim(csv_path, num_trucks=num_trucks, min_pop=min_pop, enable_finance=enable_finance)

    # Create initial random loads
    with sim_lock:
        sim = FreightSim(csv_path, num_trucks=num_trucks, min_pop=min_pop, enable_finance=enable_finance)
        for _ in range(num_loads):
            sim.create_random_load()

    return {"message": f"Simulation initialized with {num_trucks} trucks and {num_loads} loads. Finance enabled: {enable_finance}"}

# --- Get current status of trucks and loads ---
@app.get("/status")
def get_status():

    with sim_lock:
        if not sim:
            return {"trucks": [], "loads": []}

    # Build truck status list
        trucks = []
        for _, truck in sim.trucks.iterrows():
            trucks.append({
            "truck_id": truck["truck_id"],
            "lat": truck["lat"],        # current latitude
            "lon": truck["lng"],        # current longitude
            "status": truck["status"],  # Idle or Assigned
            "assigned_load": truck["assigned_load"],
            "profit": truck["profit"],
            "expense": truck["expense"],
            "net_profit": truck["profit"] - truck["expense"]
        })

    # Build load status list
        loads = []
        for _, load in sim.loads.iterrows():
            origin = sim.cities.iloc[load["origin_idx"]]
            dest = sim.cities.iloc[load["dest_idx"]]
            loads.append({
            "load_id": load["load_id"],
            "origin": origin["city"],
            "destination": dest["city"],
            "weight": load["weight"],
            "rate_per_ton": load["rate_per_ton"],
            "assigned_truck": load["assigned_truck"],
            "dest_latitude": dest["lat"],
            "dest_longitude": dest["lng"]
        })

    return {"trucks": trucks, "loads": loads}

# --- Create a new random load dynamically ---
@app.get("/create_load")
def create_load():
    with sim_lock:
        if not sim:
            return {"message": "Simulation not initialized yet."}
        sim.create_random_load()
    return {"message": "New load created"}

