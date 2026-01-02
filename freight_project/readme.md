Freight Trading Simulation 🚚📦

OwlHacks 2025 Hackathon Project

This project is a freight trading simulator I built for OwlHacks 2025. The idea is to mimic how trucks and shipments are matched in real life, so you can see who’s carrying what, track deliveries, and even create new loads on the fly. Everything is interactive and plotted on a map so you can watch the simulation happen in real-time.

Concept

Freight trading is all about moving cargo efficiently—matching shipments with transport capacity and making smart delivery decisions. I tried to capture that in this project by:

Treating trucks like transport capacity and loads like shipments.

Automatically assigning trucks to loads based on their capacity and location.

Letting you create new loads dynamically, which is like new opportunities popping up in the market.

Updating everything live so you can see trucks move toward their destinations.

It’s a simplified way to explore how freight trading works without having to charter real ships or trucks.

Project Structure
freight_project/
│
├── backend/
│   ├── app.py            # FastAPI backend that handles all the simulation endpoints
│   ├── freight_trading.py # All the simulation logic: trucks, loads, assignments, movement
│   └── requirements.txt  # Python packages: FastAPI, Uvicorn, Pandas, NumPy
│
├── frontend/
│   ├── index.html        # My web dashboard with map, inputs, and controls
│   ├── script.js         # JS code for fetching backend data and updating the map
│   └── style.css         # Styles for the dashboard UI
│
├── cli/
│   └── main.py           # Optional command-line interface version of the simulation
│
└── README.md             # This file

What each file does

backend/app.py
This is where the backend API lives. It starts the simulation, updates truck positions, and lets the frontend ask for the current status or create new loads.

backend/freight_trading.py
All the logic for the simulation happens here. Trucks, loads, assignment rules, distance calculations, and movement step-by-step are all handled in this file.

backend/requirements.txt
Lists all the Python libraries you need to run the backend (FastAPI, Uvicorn, Pandas, NumPy).

frontend/index.html
The dashboard where you control the simulation. You can input the number of trucks and loads, start the simulation, and watch everything happen on a map.

frontend/script.js
This JS handles fetching the backend data, updating truck markers, drawing lines to loads, and keeping the map live and dynamic.

frontend/style.css
Simple styling for the dashboard—makes the inputs, buttons, and map look clean.

cli/main.py
A command-line version of the simulation. Lets you run everything step by step in the terminal without using the web interface.

How to Run
Backend

Go into the backend/ folder and activate your virtual environment.

Install dependencies:

pip install -r requirements.txt


Start the FastAPI server:

uvicorn app:app --reload


Server runs on http://127.0.0.1:8000.

Frontend

Open frontend/index.html in a web browser.

Enter simulation parameters and click Start Simulation.

Click Create Random Load to add new shipments dynamically.

CLI (Optional)

Go to the cli/ folder.

Run:

python main.py

Running the Frontend

Make sure your backend FastAPI server is running (uvicorn app:app --reload) at http://127.0.0.1:8000.

Open the frontend/index.html file in a web browser. You don’t need a web server; just double-click the file or open it via your browser.

On the dashboard:

Enter simulation parameters (number of trucks, loads, minimum city population, finance tracking).

Click Start Simulation to initialize the simulation.

Use Create Random Load to add new shipments dynamically.

The map will update in real time, showing truck positions, assigned loads, and delivery paths.


cd frontend
python -m http.server 8080


Then open http://localhost:8080 in your browser.


Follow the prompts to simulate trucks and loads step by step.

Features

Real-time map showing trucks and the loads they’re carrying.

Dynamic creation of new loads to simulate changing market demand.

Automatic assignment of trucks based on capacity and location.

Dashed lines that show the path from trucks to their assigned loads.

Optional CLI version for terminal-based simulation.

Notes

I built this for OwlHacks 2025 to explore freight logistics and trading in a visual, interactive way. It’s not a real freight market, but it gives a sense of how capacity, demand, and delivery timing all interact.

