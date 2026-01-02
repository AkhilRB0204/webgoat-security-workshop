import pandas as pd
import numpy as np
import random
from math import radians, cos, sin, asin, sqrt

class FreightSim:
    def __init__(self, csv_path="uscities.csv", num_trucks=50, min_pop=50000):
        # Load cities and filter by population
        self.cities = pd.read_csv(csv_path)
        self.cities = self.cities[self.cities['population'] > min_pop].reset_index(drop=True)

        # Create trucks
        self.num_trucks = num_trucks
        self.trucks = pd.DataFrame({
            'truck_id': [f"T{i+1}" for i in range(num_trucks)],
            'city_idx': np.random.choice(self.cities.index, num_trucks),
            'capacity': np.random.randint(10, 30, num_trucks),
            'status': ['Idle'] * num_trucks,
            'assigned_load': [None] * num_trucks
        })

        self.trucks['lat'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'lat'])
        self.trucks['lng'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'lng'])
        self.trucks['city'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'city'])
        self.trucks['state'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'state_name'])
        self.trucks['zip'] = self.trucks['city_idx'].apply(lambda i: self.cities.at[i, 'zips'])

        # Loads
        self.load_counter = 1
        self.loads = pd.DataFrame(columns=['load_id', 'origin_idx', 'dest_idx', 'weight', 'assigned_truck', 'value'])

    # Haversine distance
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return 2 * asin(sqrt(a)) * 3956

    # Create a new random load with weight and value
    def create_random_load(self):
        origin_idx = random.choice(self.cities.index)
        dest_idx = random.choice([i for i in self.cities.index if i != origin_idx])
        weight = random.randint(5, 25)
        value = random.randint(10, 100)  # Profit or priority metric

        new_load = pd.DataFrame({
            'load_id': [f"L{self.load_counter}"],
            'origin_idx': [origin_idx],
            'dest_idx': [dest_idx],
            'weight': [weight],
            'assigned_truck': [None],
            'value': [value]
        })
        self.load_counter += 1
        self.loads = pd.concat([self.loads, new_load], ignore_index=True)

    # Score a truck for a load (distance / profit)
    def score(self, truck_idx, load_idx):
        truck = self.trucks.loc[truck_idx]
        load = self.loads.loc[load_idx]
        origin = self.cities.iloc[load['origin_idx']]

        dist = self.haversine(truck['lat'], truck['lng'], origin['lat'], origin['lng'])
        capacity_penalty = 0 if truck['capacity'] >= load['weight'] else 1000

        # Include profit/value in scoring
        return dist - load['value'] + capacity_penalty

    # Assign loads dynamically every step
    def assign_loads(self):
        for load_idx, load in self.loads.iterrows():
            if pd.isna(load['assigned_truck']):
                best_score = float('inf')
                best_truck_idx = None
                for truck_idx, truck in self.trucks.iterrows():
                    if truck['assigned_load'] is None:  # Only free trucks
                        s = self.score(truck_idx, load_idx)
                        if s < best_score:
                            best_score = s
                            best_truck_idx = truck_idx
                if best_truck_idx is not None:
                    self.trucks.at[best_truck_idx, 'assigned_load'] = load['load_id']
                    self.trucks.at[best_truck_idx, 'status'] = 'Assigned'
                    self.loads.at[load_idx, 'assigned_truck'] = self.trucks.at[best_truck_idx, 'truck_id']

    # Move trucks toward destination dynamically
    def update_trucks(self):
        for idx, truck in self.trucks.iterrows():
            if truck['assigned_load'] is not None:
                load = self.loads[self.loads['load_id'] == truck['assigned_load']].iloc[0]
                dest = self.cities.iloc[load['dest_idx']]

                # Move halfway closer each step
                truck_lat = truck['lat'] + (dest['lat'] - truck['lat']) * 0.5
                truck_lng = truck['lng'] + (dest['lng'] - truck['lng']) * 0.5
                self.trucks.at[idx, 'lat'] = truck_lat
                self.trucks.at[idx, 'lng'] = truck_lng

                # Check arrival
                if self.haversine(truck_lat, truck_lng, dest['lat'], dest['lng']) < 0.1:
                    self.trucks.at[idx, 'status'] = 'Idle'
                    self.trucks.at[idx, 'assigned_load'] = None
                    # Remove load
                    self.loads = self.loads[self.loads['load_id'] != load['load_id']]
