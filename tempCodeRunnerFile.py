def check_plants():
    plants = load_data(PLANT_DB)
    maintenance = load_data(MAINTENANCE_DB)

    if isinstance(maintenance, list):
        maintenance = {}

    now = datetime.now()
    print("\n🌱 Plants List:\n")
    for plant in plants:

        # Normalize keys
        plant_id = str(plant.get('plantID'))
        plant_name = plant.get('plant_name')

        # Normalize care schedule fallback
        if 'care_schedule' in plant:
            care = plant['care_schedule']
        else:
            # fallback for simpler plants
            care = {
                'water_every_hours': int(plant.get('water_schedule', 24)),
                'fertilize_every_hours': 168,  # default weekly fertilizing
                'harvest_after_hours': 1008   # default 6 weeks harvest
            }

        state = maintenance.get(plant_id, {
            'last_watered': now.isoformat(),
            'last_fertilized': now.isoformat(),
            'planted_on': now.isoformat()
        })

        # Last actions timestamps
        last_watered = datetime.fromisoformat(state['last_watered'])
        last_fertilized = datetime.fromisoformat(state['last_fertilized'])
        planted_on = datetime.fromisoformat(state['planted_on'])

        # Calculate time remaining
        next_water = last_watered + timedelta(hours=care['water_every_hours'])
        next_fertilize = last_fertilized + timedelta(hours=care['fertilize_every_hours'])
        harvest_time = planted_on + timedelta(hours=care['harvest_after_hours'])

        print(f"\nPlant: {plant_name}")
        print(f"💧 Water in: {(next_water - now)}")
        print(f"🌱 Fertilize in: {(next_fertilize - now)}")
        print(f"🧺 Harvest in: {(harvest_time - now)}")

        if next_water <= now:
            print("⚠️ Needs watering now!")
        if next_fertilize <= now:
            print("⚠️ Needs fertilizing now!")
        if harvest_time <= now:
            print("✅ Ready for harvest!")

        print("\n")