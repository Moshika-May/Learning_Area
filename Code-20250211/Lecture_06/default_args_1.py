def production_cost(labor_cost, material_cost=1000, fixed_cost=1000):
    total_cost = material_cost + labor_cost + fixed_cost
    return total_cost

def main():
    total_cost = production_cost(500)
    print(f"Total Production Cost: {total_cost}")

    total_cost = production_cost(500, 500)
    print(f"Total Production Cost: {total_cost}")

    total_cost = production_cost(500, 500, 500)
    print(f"Total Production Cost: {total_cost}")

main()
