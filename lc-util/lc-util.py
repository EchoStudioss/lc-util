import os
import re
import time


ITEMS_OUTPUT_FILE = "ox_inventory_items.txt" 
VEHICLES_OUTPUT_FILE = "qb_vehicles.txt"  


def add_items_from_images(folder_path):
    items = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):
            item_name = os.path.splitext(file_name)[0]  
            item_label = item_name.capitalize() 
            item_weight = 100  # Default weight, can be customized
            items.append({
                "name": item_name,
                "label": item_label,
                "weight": item_weight
            })
    return items

def add_items_from_notepad(file_path):
    items = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(',')
                if len(parts) >= 3:
                    items.append({
                        "name": parts[0].strip(),
                        "label": parts[1].strip(),
                        "weight": int(parts[2].strip())
                    })
    return items


def add_items_from_csv(file_path):
    import csv 
    items = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({
                "name": row['name'],
                "label": row['label'],
                "weight": int(row['weight'])
            })
    return items

def save_items_to_text_file(items):
    with open(ITEMS_OUTPUT_FILE, 'w') as file:
        for item in items:
            item_entry = f'{{name = "{item["name"]}", label = "{item["label"]}", weight = {item["weight"]}}},\n'
            file.write(item_entry)
    print(f"Items saved to {ITEMS_OUTPUT_FILE}")
    input("Press Enter to continue...")  


def add_vehicles_from_meta(folder_path):
    vehicles = []
    model_name_pattern = re.compile(r'<modelName>(\w+)</modelName>')  


    for file_name in os.listdir(folder_path):
        if file_name == 'vehicles.meta': 
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                content = file.read()  
                matches = model_name_pattern.findall(content)  


                for match in matches:
                    vehicle_entry = {
                        "model": match.lower(),  # Model name in lowercase
                        "name": match.capitalize(),  # Default name, can be customized
                        "brand": "Unknown",  # Default brand, can be changed manually
                        "price": 20000,  # Default price, can be customized
                        "category": "unknown",  # Default category
                        "type": "automobile",  # Default type
                        "shop": "pdm"  # Default shop
                    }
                    vehicles.append(vehicle_entry)  # Append vehicle entry to the list
    return vehicles

def save_vehicles_to_text_file(vehicles):
    with open(VEHICLES_OUTPUT_FILE, 'w') as file:
        for vehicle in vehicles:
            vehicle_entry = (f"{{ model = '{vehicle['model']}', name = '{vehicle['name']}', "
                             f"brand = '{vehicle['brand']}', price = {vehicle['price']}, "
                             f"category = '{vehicle['category']}', type = '{vehicle['type']}', "
                             f"shop = '{vehicle['shop']}' }},\n")
            file.write(vehicle_entry)
    print(f"Vehicles saved to {VEHICLES_OUTPUT_FILE}")
    input("Press Enter to continue...") 


def return_to_main_menu():
    input("Returning to main menu... Press Enter to continue.")
    main()

def main():
    while True:  
        print("\nChoose what you'd like to add:")
        print("1. Add items (Ox Inventory)")
        print("2. Add vehicles (QB-Core)")
        print("3. Exit")

        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == '1':
            print("Choose how you'd like to add items:")
            print("1. From PNG images in a folder")
            print("2. From a notepad file (text file)")
            print("3. From a CSV file")
            item_choice = input("Enter 1, 2, or 3: ").strip()
            items = []

            if item_choice == '1':
                folder_path = input("Enter the path to the folder with PNG image files: ").strip()
                items = add_items_from_images(folder_path)
            elif item_choice == '2':
                file_path = input("Enter the path to the notepad file: ").strip()
                items = add_items_from_notepad(file_path)
            elif item_choice == '3':
                file_path = input("Enter the path to the CSV file: ").strip()
                items = add_items_from_csv(file_path)
            else:
                print("Invalid choice")
                continue  

            if items:
                save_items_to_text_file(items)
            else:
                print("No items found to add.")
                input("Press Enter to return to the main menu...") 

            return_to_main_menu()

        elif choice == '2':
            folder_path = input("Enter the path to the folder with vehicle.meta files: ").strip()
            vehicles = add_vehicles_from_meta(folder_path)

            if vehicles:
                save_vehicles_to_text_file(vehicles)
            else:
                print("No vehicles found in the meta files.")
                input("Press Enter to return to the main menu...")

            return_to_main_menu()

        elif choice == '3':
            print("Exiting...")
            break  

        else:
            print("Invalid choice")
            time.sleep(2)  

    input("Press Enter to exit...")  

if __name__ == "__main__":
    main()
