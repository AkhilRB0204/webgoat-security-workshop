// Initialize Leaflet map centered on the US
const map = L.map('map').setView([39.5, -98.35], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let truckMarkers = {};
let loadLines = {};

// Function to refresh truck positions and load lines from backend
async function refresh() {
    const res = await fetch("http://127.0.0.1:8000/status");
    const data = await res.json();

    // --- Update or create truck markers ---
    data.trucks.forEach(truck => {
        if (truckMarkers[truck.truck_id]) {
            // Move existing marker to new position
            truckMarkers[truck.truck_id].setLatLng([truck.lat, truck.lon]);
            truckMarkers[truck.truck_id].bindPopup(`${truck.truck_id} - ${truck.status}`);
        } else {
            // Create a new marker
            truckMarkers[truck.truck_id] = L.circleMarker([truck.lat, truck.lon], {
                radius: 6,
                color: truck.status === "Idle" ? "green" : "orange" // color by status
            }).addTo(map)
              .bindPopup(`${truck.truck_id} - ${truck.status}`);
        }
    });

    // --- Draw dynamic lines from truck → load destination ---
    data.loads.forEach(load => {
        const lineId = load.load_id;
        // Find the truck assigned to this load
        const truck = data.trucks.find(t => t.truck_id === load.assigned_truck);

        if (!truck) return; // skip if no truck assigned yet

        const start = [truck.lat, truck.lon];                   // truck current position
        const end = [load.dest_latitude, load.dest_longitude];  // destination

        if (!loadLines[lineId]) {
            // Create polyline if it doesn't exist
            loadLines[lineId] = L.polyline([start, end], {
                color: "blue",
                weight: 3,
                dashArray: '5, 5'
            }).addTo(map);
        } else {
            // Update existing line dynamically
            loadLines[lineId].setLatLngs([start, end]);
        }
    });

    // --- Remove delivered load lines ---
    Object.keys(loadLines).forEach(lineId => {
        if (!data.loads.some(l => l.load_id === lineId)) {
            map.removeLayer(loadLines[lineId]);
            delete loadLines[lineId];
        }
    });
}

// --- Function to start simulation with dynamic user inputs ---
async function startSimulation() {
    const numTrucks = document.getElementById("numTrucks").value;
    const numLoads = document.getElementById("numLoads").value;
    const minPop = document.getElementById("minPop").value;

    // Call backend endpoint to initialize simulation
    await fetch(`http://127.0.0.1:8000/init?num_trucks=${numTrucks}&num_loads=${numLoads}&min_pop=${minPop}`);
    alert("Simulation started!");
}

// --- Function to create a new random load dynamically ---
async function createLoad() {
    await fetch("http://127.0.0.1:8000/create_load");
    refresh();  // force map update right after creating a load
}

// --- Auto-refresh every 1 second ---
setInterval(refresh, 1000);
