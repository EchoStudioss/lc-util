# LuaCat: Vehicle and Item Management Script for FiveM Servers

designed to automate vehicle and item management for FiveM servers. It simplifies the process of extracting vehicle model names from `vehicles.meta` files and adding items to Ox Inventory, ensuring better resource management and faster configuration.

## Features
- **Extract Vehicle Models:** Scans `vehicles.meta` files and extracts `<modelName>` values, saving them in a format compatible with QB-Core's `shared/vehicles.lua`.
- **Add Items to Ox Inventory:** Supports adding items from PNG images, Notepad files, or CSV files, and formats them for use in Ox Inventory.
- **Simple Command-Line Interface:** Choose between adding vehicles or items with simple prompts.
- **Customization:** Modify vehicle details (price, brand, category) or item details (weight, labels) easily.

---

## Requirements
- **Python 3.x**
- A folder containing `vehicles.meta` files for vehicle extraction
- PNG, CSV, or text files for adding items

---

## How to Use

### 1. Clone the Repository
First, clone this repository to your local machine:

```bash
git clone https://github.com/LuaCatt/LC-Util.git
cd LC-Util
```
### 2. Install Python
Make sure you have Python 3.x installed. If you don’t, you can download and install it from the official [Python website](https://www.python.org/downloads/).

### 3. Run the Script
Run the script from your terminal or command prompt

### 4. Choose Your Action
When the script starts, you’ll be prompted to choose what you’d like to do:
```bash
Choose what you'd like to add:
1. Add items (Ox Inventory)
2. Add vehicles (QB-Core)
3. Exit
```
### 5. Adding Items to Ox Inventory
If you choose to add items, you can add them using one of three input methods:

PNG Images: Provide the path to a folder of PNG images representing the items.
Notepad File: Provide the path to a text file where each line contains an item, its label, and its weight.
CSV File: Provide the path to a CSV file with columns for name, label, and weight.
The script will format these items and save them into a file called ox_inventory_items.txt for integration with Ox Inventory.

### 6. Extracting Vehicle Models from vehicles.meta
If you choose to extract vehicles, provide the path to the folder containing your vehicles.meta files. The script will extract all <modelName> tags and save them into a file called qb_vehicles.txt, ready for use in QB-Core's shared/vehicles.lua.

### 7. View and Modify Output
Items: The extracted items are saved in ox_inventory_items.txt.
Vehicles: The vehicle models are saved in qb_vehicles.txt.
Feel free to modify these files as needed before adding them to your FiveM server.
