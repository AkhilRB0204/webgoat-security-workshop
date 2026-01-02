from freight_trading import FreightSim

def main():
    print("Freight Route Trading Simulator")

    # Ask user for input values
    num_trucks = int(input("Enter number of trucks: "))
    num_steps = int(input("Enter number of simulation steps: "))
    loads = int(input("Enter number of loads to create: "))
    min_pop = int(input("Enter minimum population for city selection: "))

    # Start simulation
    sim = FreightSim("uscities.csv", num_trucks=num_trucks, min_pop=min_pop)

    # Create loads
    for _ in range(num_loads):
        sim.create_random_load()

    # Assign loads to trucks
    sim.assign_loads()

    # Simulate step by step
    for step in range(num_steps):
        print(f"\n--- Step {step+1} ---")
        sim.update_trucks()
        print(sim.trucks[['truck_id','city','status','assigned_load']])
        print(sim.loads[['load_id','weight','assigned_truck']])

if __name__ == "__main__":
    main()
