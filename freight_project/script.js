let cities = [];

// Load CSV file dynamically
Papa.parse("uscities.csv", {
  download: true,
  header: true,
  complete: (results) => {
    cities = results.data;
    console.log("Loaded cities:", cities.length);
  }
});

// Pick a random city filtered by min population
function randomCity(minPop) {
  const filtered = cities.filter(c => parseInt(c.population) > minPop);
  return filtered[Math.floor(Math.random() * filtered.length)];
}

// Haversine distance calculator (miles)
function haversine(lat1, lon1, lat2, lon2) {
  const R = 3956;
  const toRad = x => (x * Math.PI) / 180;

  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2)**2 +
    Math.cos(toRad(lat1)) *
    Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2)**2;

  return 2 * R * Math.asin(Math.sqrt(a));
}

function startSimulation() {
  const numTrucks = parseInt(document.getElementById("trucks").value);
  const numLoads = parseInt(document.getElementById("loads").value);
  const minPop = parseInt(document.getElementById("min_pop").value);

  let output = "";

  //----------------------------------
  // 1. Create trucks
  //----------------------------------
  let trucks = [];
  for (let i = 0; i < numTrucks; i++) {
    let c = randomCity(minPop);
    trucks.push({
      id: "T" + (i+1),
      city: c.city,
      lat: parseFloat(c.lat),
      lon: parseFloat(c.lng),
      status: "Idle",
      capacity: Math.floor(Math.random() * 20) + 10
    });
  }

  //----------------------------------
  // 2. Create loads
  //----------------------------------
  let loads = [];
  for (let i = 0; i < numLoads; i++) {
    let origin = randomCity(minPop);
    let dest = randomCity(minPop);

    loads.push({
      id: "L" + (i+1),
      origin: origin.city,
      dest: dest.city,
      latO: parseFloat(origin.lat),
      lonO: parseFloat(origin.lng),
      latD: parseFloat(dest.lat),
      lonD: parseFloat(dest.lng),
      weight: Math.floor(Math.random() * 20) + 5
    });
  }

  //----------------------------------
  // 3. Assign loads to trucks
  //----------------------------------
  loads.forEach(load => {
    let bestTruck = null;
    let bestScore = Infinity;

    trucks.forEach(truck => {
      if (truck.status === "Idle") {
        if (truck.capacity < load.weight) return;

        let dist = haversine(truck.lat, truck.lon, load.latO, load.lonO);

        if (dist < bestScore) {
          bestScore = dist;
          bestTruck = truck;
        }
      }
    });

    if (bestTruck) {
      bestTruck.status = "Assigned → " + load.id;
      load.assigned = bestTruck.id;
    } else {
      load.assigned = "NO AVAILABLE TRUCK";
    }
  });

  //----------------------------------
  // Output
  //----------------------------------
  output += "🚛 TRUCKS:\n";
  trucks.forEach(t => {
    output += `${t.id} — ${t.city} — ${t.status} — cap ${t.capacity}\n`;
  });

  output += "\n📦 LOADS:\n";
  loads.forEach(l => {
    output += `${l.id} — ${l.origin} → ${l.dest} — weight ${l.weight} — assigned: ${l.assigned}\n`;
  });

  document.getElementById("output").innerText = output;
}
