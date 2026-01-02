from backend.freight_trading import FreightSim

def main():
    print("🚚 Freight Route Trading Simulator (with Finance Tracking)")

    # Ask user for input values
    num_trucks = int(input("Enter number of trucks: "))
    num_steps = int(input("Enter number of simulation steps: "))
    loads = int(input("Enter number of loads to create: "))
    min_pop = int(input("Enter minimum population for city selection: "))

    # Start simulation
    sim = FreightSim("backend/uscities.csv", num_trucks=num_trucks, min_pop=min_pop)

    # Create loads
    for _ in range(loads):
        sim.create_random_load()

    # Assign loads to trucks
    sim.assign_loads()

    # Simulate step by step
    for step in range(num_steps):
        print(f"\n--- Simulation Step {step+1} ---")
        sim.update_trucks()

        # print financial summary
        total_revenue = sim.total_revenue()
        total_expense = sim.total_expense()
        net_profit = total_revenue - total_expense

        print(f"💰 Revenue: ${total_revenue:.2f} | Expenses: ${total_expense:.2f} | Net Profit: ${net_profit:.2f}")
    
    print("\n✅ Simulation complete!")
    print("Final Truck Profits:")
    for _, truck in sim.trucks.iterrows():
        print(f"Truck {truck['truck_id']}: Profit = ${truck['profit']:.2f}")


if __name__ == "__main__":
    main()