Freight Trading Simulation 🚚📦

OwlHacks 2026 Hackathon Project

This project is a freight trading simulation that models the buying, selling, and assignment of cargo (loads) to transport capacity (trucks) across cities in the U.S. It provides an interactive map-based dashboard where users can initialize fleets, create new loads, and watch dynamic assignments in real-time, reflecting simplified freight market operations.

Concept

Freight trading in the real world involves matching cargo with transport capacity, managing shipments efficiently, and sometimes speculating on freight price movements. In this simulation:

Trucks represent available transport capacity.

Loads represent shipments that need to be delivered.

Truck assignment simulates the market decision of allocating transport capacity to maximize efficiency or profit.

Dynamic load creation mimics new market opportunities or volatile demand.

Real-time updates simulate continuous freight market activity.

This approach allows participants to explore freight logistics, trading, and decision-making in a simplified, visual way.

Project Structure
freight_project/
│
├── backend/
│   ├── app.py            # FastAPI backend handling simulation endpoints
│   ├── freight_trading.py # Core simulation logic: trucks, loads, assignment, and movement
│   └── requirements.txt  # Python dependencies: fastapi, uvicorn, pandas, numpy
│
├── frontend/
│   ├── index.html        # Web dashboard with map, inputs, and controls
│   ├── script.js         # JS logic for fetching backend data, updating the map, and drawing lines
│   └── style.css         # Styles for dashboard UI
│
├── cli/
│   └── main.py           # Optional CLI to run the simulation step by step in the terminal
│
└── README.md             # This file

File Descriptions

backend/app.py
This is the FastAPI backend that exposes API endpoints for the frontend. It allows users to initialize the simulation, fetch real-time truck and load statuses, and create new loads dynamically.

backend/freight_trading.py
Contains the main simulation logic. It defines trucks, loads, assignment rules, distance calculations, and updates truck positions step-by-step, mimicking freight market operations.

backend/requirements.txt
Lists all Python packages required to run the backend, including FastAPI, Uvicorn, Pandas, and NumPy.

frontend/index.html
The interactive web dashboard that visualizes the simulation. Users can input parameters, start the simulation, and see trucks and loads dynamically plotted on a U.S. map.

frontend/script.js
Handles the dynamic behavior of the dashboard: fetching backend data, updating truck markers, drawing lines to loads, and refreshing the map every second.

frontend/style.css
Defines the styling of the dashboard, including layout, buttons, input fields, and the output console for truck and load statuses.

cli/main.py
Optional command-line interface to run the simulation in the terminal. Users can input parameters, create loads, assign trucks, and simulate steps without using the web interface.

How to Run
Backend

Navigate to backend/ and activate your virtual environment.

Install dependencies:

pip install -r requirements.txt


Start the FastAPI server:

uvicorn app:app --reload


Server runs on: http://127.0.0.1:8000

Frontend

Open frontend/index.html in a web browser (Chrome or Firefox recommended).

Enter simulation parameters and click Start Simulation.

Click Create Random Load to add new shipments dynamically.

CLI (Optional)

Navigate to cli/ folder.

Run:

python main.py


Follow prompts to simulate trucks and loads step by step in the terminal.

Features

Real-time map visualization of trucks and their assigned loads.

Dynamic creation of new loads to simulate a changing market.

Automatic assignment of trucks to loads based on capacity and proximity.

Visual tracking of deliveries with moving trucks and dashed lines connecting to destinations.

Optional CLI for terminal-based simulation.

Hackathon Notes

This project was developed for OwlHacks 2026. It demonstrates:

Simulation of freight trading decisions in a simplified market.

Integration of Python backend, Pandas data processing, FastAPI APIs, and interactive frontend visualization with Leaflet.js.

Dynamic, real-time updates reflecting freight operations in a gamified environment.
