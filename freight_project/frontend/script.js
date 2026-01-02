const map = L.map('map').setView([39.5, -98.35], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let truckMarkers = {};
let loadLines = {};

async function refresh() {
    const res = await fetch("http://127.0.0.1:8000/status");
    const data = await res.json();

    // Trucks
    data.trucks.forEach(truck => {
        if (truckMarkers[truck.truck_id]) {
            truckMarkers[truck.truck_id].setLatLng([truck.lat, truck.lon]);
            truckMarkers[truck.truck_id].bindPopup(`${truck.truck_id} - ${truck.status}`);
        } else {
            truckMarkers[truck.truck_id] = L.circleMarker([truck.lat, truck.lon], {
                radius: 6,
                color: truck.status === "Idle" ? "green" : "orange"
            }).addTo(map).bindPopup(`${truck.truck_id} - ${truck.status}`);
        }
    });

    // Loads (polylines)
    data.loads.forEach(load => {
        const lineId = load.load_id;
        const origin = [load.latO || load.dest_lat, load.lonO || load.dest_lon];
        const dest = [load.dest_lat, load.dest_lon];

        if (!loadLines[lineId]) {
            loadLines[lineId] = L.polyline([origin, dest], {
                color: "orange",
                weight: 2,
                dashArray: '5,5'
            }).addTo(map);
        }
    });

    // Remove delivered loads
    Object.keys(loadLines).forEach(lineId => {
        if (!data.loads.some(l => l.load_id === lineId)) {
            map.removeLayer(loadLines[lineId]);
            delete loadLines[lineId];
        }
    });
}

// Initialize simulation
async function startSimulation() {
    const numTrucks = document.getElementById("numTrucks").value;
    const numLoads = document.getElementById("numLoads").value;
    const minPop = document.getElementById("minPop").value;

    await fetch(`http://127.0.0.1:8000/init?num_trucks=${numTrucks}&num_loads=${numLoads}&min_pop=${minPop}`);
    alert("Simulation started!");
}

async function createLoad() {
    await fetch("http://127.0.0.1:8000/create_load");
}

// Auto-refresh every 1 second
setInterval(refresh, 1000);
