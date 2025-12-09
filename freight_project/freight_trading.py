import pandas as pd
import numpy as np
import random
from math import radians, cos, sin, asin, sqrt

class FreightSim:
    def __init__(self, csv_path="uscities.csv", num_trucks=50, min_pop=50000):
        # Load all US cities from the CSV file
        self.cities = pd.read_csv(csv_path)

        # Keep only "big" cities with population above a threshold
        self.cities = self.cities[self.cities['population'] > min_pop].reset_index(drop=True)
        
        # Create a fleet of trucks
        self.num_trucks = num_trucks
        self.trucks = pd.DataFrame({
            'truck_id': [f"T{i+1}" for i in range(num_trucks)],   # Truck names T1, T2, ...
            'city_idx': np.random.choice(self.cities.index, num_trucks),  # Start trucks in random cities
            'capacity': np.random.randint(10, 30, num_trucks),    # Each truck can carry 10–30 tons
            'status': ['Idle'] * num_trucks,                      # Idle = waiting for a job
            'assigned_load': [None] * num_trucks                  # No load assigned yet
        })

        # Add city details to each truck so we know where it is
        self.trucks['lat'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'lat'])
        self.trucks['lng'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'lng'])
        self.trucks['city'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'city'])
        self.trucks['state'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'state_name'])
        self.trucks['zip'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'zips'])
        
        # Empty table of shipments (loads) to start
        self.load_counter = 1
        self.loads = pd.DataFrame(columns=['load_id', 'origin_idx', 'dest_idx', 'weight', 'assigned_truck'])
    
    # --- Function to calculate distance between two points on Earth ---
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # Convert lat/lon from degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # Formula for great-circle distance
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956  # radius of Earth in miles
        return c * r

    # --- How good is this truck for this load? ---
    def score(self, truck_idx, load_idx):
        truck = self.trucks.loc[truck_idx]
        load = self.loads.loc[load_idx]
        origin = self.cities.iloc[load['origin_idx']]

        # Distance from truck to the load’s pickup city
        dist = self.haversine(truck['lat'], truck['lng'], origin['lat'], origin['lng'])

        # If truck is too small for the load, make its score terrible
        capacity_penalty = 0 if truck['capacity'] >= load['weight'] else 1000

        return dist + capacity_penalty

    # --- Make a new random shipment ---
    def create_random_load(self):
        # Pick a random city as the origin
        origin_idx = random.choice(self.cities.index)
        # Pick a different random city as the destination
        dest_idx = random.choice([i for i in self.cities.index if i != origin_idx])
        # Random weight between 5–25 tons
        weight = random.randint(5, 25)

        # Store this load in our loads table
        new_load = pd.DataFrame({
            'load_id': [f"L{self.load_counter}"],
            'origin_idx': [origin_idx],
            'dest_idx': [dest_idx],
            'weight': [weight],
            'assigned_truck': [None]
        })
        self.load_counter += 1
        self.loads = pd.concat([self.loads, new_load], ignore_index=True)
        
        # Print for the user
        origin_city = self.cities.iloc[origin_idx]
        dest_city = self.cities.iloc[dest_idx]
        print(f"🆕 New Load {new_load['load_id'][0]}: {weight} tons "
              f"from {origin_city['city']}, {origin_city['state_name']} "
              f"to {dest_city['city']}, {dest_city['state_name']}")

    # --- Match available trucks to loads ---
    def assign_loads(self):
        for load_idx, load in self.loads.iterrows():
            if pd.isna(load['assigned_truck']):
                best_score = float('inf')
                best_truck_idx = None
                # Check every truck to see which one is best
                for truck_idx, truck in self.trucks.iterrows():
                    if truck['assigned_load'] is None:  # only free trucks
                        s = self.score(truck_idx, load_idx)
                        if s < best_score:
                            best_score = s
                            best_truck_idx = truck_idx
                # Assign best truck found
                if best_truck_idx is not None:
                    self.trucks.at[best_truck_idx, 'assigned_load'] = load['load_id']
                    self.trucks.at[best_truck_idx, 'status'] = 'Assigned'
                    self.loads.at[load_idx, 'assigned_truck'] = self.trucks.at[best_truck_idx, 'truck_id']
                    truck_info = self.trucks.loc[best_truck_idx]
                    print(f"🚚 Assigned Load {load['load_id']} to Truck {truck_info['truck_id']} "
                          f"at {truck_info['city']}, {truck_info['state']}")

    # --- Move trucks step by step toward destination ---
    def update_trucks(self):
        for idx, truck in self.trucks.iterrows():
            if truck['assigned_load'] is not None:
                load = self.loads[self.loads['load_id'] == truck['assigned_load']].iloc[0]
                dest = self.cities.iloc[load['dest_idx']]

                # Move halfway closer to destination each time we call this
                truck_lat = truck['lat']
                truck_lng = truck['lng']
                truck_lat += (dest['lat'] - truck_lat) * 0.5
                truck_lng += (dest['lng'] - truck_lng) * 0.5

                # Update truck’s position
                self.trucks.at[idx, 'lat'] = truck_lat
                self.trucks.at[idx, 'lng'] = truck_lng

                # If truck has basically arrived
                if self.haversine(truck_lat, truck_lng, dest['lat'], dest['lng']) < 0.1:
                    self.trucks.at[idx, 'status'] = 'Idle'
                    self.trucks.at[idx, 'assigned_load'] = None
                    print(f"✅ Truck {truck['truck_id']} arrived at {dest['city']}, {dest['state_name']}")
                    # Remove load (delivered)
                    self.loads = self.loads[self.loads['load_id'] != load['load_id']]

# --- Example simulation run ---
if __name__ == "__main__":
    sim = FreightSim("uscities.csv", num_trucks=10)

    # Make 5 random shipments
    for _ in range(5):
        sim.create_random_load()

    # Assign trucks to those shipments
    sim.assign_loads()

    # Move trucks step by step until some deliveries finish
    for _ in range(10):
        sim.update_trucks()