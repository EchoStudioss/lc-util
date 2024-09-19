import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv

ITEMS_OUTPUT_FILE = "items_output.txt"
VEHICLES_OUTPUT_FILE = "vehicles_output.txt"
WEAPONS_OUTPUT_FILE = "weapons_output.txt"

script_dir = os.path.dirname(os.path.abspath(__file__))

ITEMS_OUTPUT_FILE = os.path.join(script_dir, ITEMS_OUTPUT_FILE)
VEHICLES_OUTPUT_FILE = os.path.join(script_dir, VEHICLES_OUTPUT_FILE)
WEAPONS_OUTPUT_FILE = os.path.join(script_dir, WEAPONS_OUTPUT_FILE)

BACKGROUND_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
TEXT_COLOR = "#ecf0f1"
FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 12)

ammo_conversion = {
    'ox_inventory': {
        'AMMO_PISTOL': 'ammo-9',
        'AMMO_SMG': 'ammo-45',
        'AMMO_RIFLE': 'ammo-rifle'
    },
    'qbcore': {
        'ammo-9': 'AMMO_PISTOL',
        'ammo-45': 'AMMO_SMG',
        'ammo-rifle': 'AMMO_RIFLE'
    }
}

def on_enter(event):
    event.widget['background'] = '#2980b9'

def on_leave(event):
    event.widget['background'] = BUTTON_COLOR

def add_items_from_images(folder_path):
    items = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):
            item_name = os.path.splitext(file_name)[0]
            item_label = item_name.capitalize()
            item_weight = 100
            items.append({
                "name": item_name,
                "label": item_label,
                "weight": item_weight,
                "stack": True,
                "close": True
            })
    return items

def add_items(item_type):
    if item_type == 'images':
        folder_path = filedialog.askdirectory()  # For images, select a folder
        if folder_path:
            items = add_items_from_images(folder_path)
        else:
            messagebox.showerror("Error", "No folder selected.")
            return
    elif item_type == 'notepad':
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])  # For notepad, select a file
        if file_path:
            items = add_items_from_notepad(file_path)
        else:
            messagebox.showerror("Error", "No file selected.")
            return
    elif item_type == 'csv':
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])  # For CSV, select a file
        if file_path:
            items = add_items_from_csv(file_path)
        else:
            messagebox.showerror("Error", "No file selected.")
            return
    else:
        messagebox.showerror("Error", "Invalid item type.")
        return

    save_items_to_text_file(items)  # Save items after they have been successfully added

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
                        "weight": int(parts[2].strip()),
                        "stack": True,
                        "close": True
                    })
    return items

def add_items_from_csv(file_path):
    items = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({
                "name": row['name'],
                "label": row['label'],
                "weight": int(row['weight']),
                "stack": True,
                "close": True
            })
    return items

def save_items_to_text_file(items):
    framework = selected_framework.get()
    
    try:
        with open(ITEMS_OUTPUT_FILE, 'w') as file:
            for item in items:
                if framework == 'ox_inventory':
                    item_entry = (
                        f"['{item['name']}'] = {{\n"
                        f"    label = '{item['label']}',\n"
                        f"    weight = {item['weight']},\n"
                        f"    stack = true,\n"
                        f"    close = true,\n"
                        f"}}}},\n"  # Escaping curly braces
                    )
                elif framework == 'qbcore':
                    item_entry = (
                        f"{item['name']} = {{ name = '{item['name']}', label = '{item['label']}', weight = {item['weight']}, type = 'item', image = '{item['name']}.png', unique = false, useable = true, shouldClose = true, description = 'Description for {item['label']}' }},\n"
                    )
                file.write(item_entry)
        messagebox.showinfo("Success", f"Items saved to {ITEMS_OUTPUT_FILE}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving items: {e}")

def save_weapons_to_text_file(weapons):
    framework = selected_framework.get()
    
    try:
        with open(WEAPONS_OUTPUT_FILE, 'w') as file:
            for weapon in weapons:
                ammo_type = ammo_conversion[framework].get(weapon['ammotype'], weapon['ammotype'])
                
                if framework == 'ox_inventory':
                    weapon_entry = (
                        f"['{weapon['name']}'] = {{\n"
                        f"    label = '{weapon['label']}',\n"
                        f"    weight = {weapon['weight']},\n"
                        f"    durability = {weapon['durability']},\n"
                        f"    ammoname = '{ammo_type}',\n"
                        f"}}}},\n"
                    )
                elif framework == 'qbcore':
                    # Ensure we have the correct ammo type
                    ammotype = ammo_conversion[framework].get(weapon['ammotype'], 'UNKNOWN_TYPE')
                    # Default values for weapontype and damagereason if they are not provided
                    weapontype = weapon.get('weapontype', 'UNKNOWN_TYPE')
                    damagereason = weapon.get('damagereason', 'UNKNOWN_REASON')
                    weapon_entry = (
                        f"[{weapon['name']}] = {{\n"
                        f"    name = '{weapon['name']}',\n"
                        f"    label = '{weapon['label']}',\n"
                        f"    weapontype = '{weapontype}',\n"
                        f"    ammotype = '{ammotype}',\n"
                        f"    damagereason = '{damagereason}'\n"
                        f"}}}},\n"
                    )
                file.write(weapon_entry)
        messagebox.showinfo("Success", f"Weapons saved to {WEAPONS_OUTPUT_FILE}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving weapons: {e}")

def add_weapons_from_meta_recursive(folder_path):
    weapons = []
    weapon_name_pattern = re.compile(r'<Name>(\w+)</Name>')
    ammo_type_pattern = re.compile(r'<AmmoInfo ref="(\w+)" />')
    
    for root, dirs, files in os.walk(folder_path):  
        for file_name in files:
            if file_name == 'weapons.meta':  
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")  # Debugging statement
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"Content of {file_path}:")  # Debugging statement
                    print(content)  # Debugging statement
                    
                    weapon_matches = weapon_name_pattern.findall(content)
                    ammo_matches = ammo_type_pattern.findall(content)
                    
                    print(f"Weapon matches: {weapon_matches}")  # Debugging statement
                    print(f"Ammo matches: {ammo_matches}")  # Debugging statement
                    
                    for weapon_name in weapon_matches:
                        ammo_type = ammo_matches[0] if ammo_matches else 'UNKNOWN'
                        weapon_entry = {
                            "name": weapon_name.lower(),
                            "label": weapon_name.capitalize(),
                            "weight": 3000,
                            "durability": 0.05,
                            "ammotype": ammo_type,
                            "weapontype": 'UNKNOWN_TYPE',  # Ensure this is handled or provided
                            "damagereason": 'UNKNOWN_REASON'  # Ensure this is handled or provided
                        }
                        weapons.append(weapon_entry)
                        
                        # Remove the first ammo match to ensure each weapon gets its ammo
                        if ammo_matches:
                            ammo_matches.pop(0)
    return weapons


def select_folder_and_add_weapons():
    folder_path = filedialog.askdirectory() 
    if folder_path:
        weapons = add_weapons_from_meta_recursive(folder_path)  
        if weapons:
            save_weapons_to_text_file(weapons)
        else:
            messagebox.showinfo("No Data", "No weapon data found in the selected folder.")
    else:
        messagebox.showerror("Error", "No folder selected.")

def select_folder_and_add_vehicles():
    folder_path = filedialog.askdirectory() 
    if folder_path:
        vehicles = add_vehicles_from_meta_recursive(folder_path)  
        save_vehicles_to_text_file(vehicles)
    else:
        messagebox.showerror("Error", "No folder selected.")

def update_buttons():
    framework = selected_framework.get()
    if framework == 'ox_inventory':
        add_items_btn.pack(side='left', padx=5, pady=5)
        add_weapons_btn.pack(side='left', padx=5, pady=5)
        add_vehicles_btn.pack_forget()
    elif framework == 'esx':
        add_items_btn.pack_forget()
        add_weapons_btn.pack_forget()
        add_vehicles_btn.pack(side='left', padx=5, pady=5)
    elif framework == 'qbcore':
        add_items_btn.pack(side='left', padx=5, pady=5)
        add_weapons_btn.pack(side='left', padx=5, pady=5)
        add_vehicles_btn.pack(side='left', padx=5, pady=5)

# GUI setup
root = tk.Tk()
root.title("Script Generator")
root.geometry("600x400")
root.configure(bg=BACKGROUND_COLOR)

# Framework selection
selected_framework = tk.StringVar(value='ox_inventory')
framework_label = tk.Label(root, text="Select Framework:", font=FONT_LABEL, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
framework_label.pack(pady=10)

frameworks = ['ox_inventory', 'esx', 'qbcore']
for framework in frameworks:
    rb = tk.Radiobutton(root, text=framework, variable=selected_framework, value=framework, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=FONT_LABEL, selectcolor=BUTTON_COLOR)
    rb.pack(anchor='w', padx=20)

# Buttons
add_items_btn = tk.Button(root, text="Add Items", command=lambda: add_items('images'), bg=BUTTON_COLOR, fg=TEXT_COLOR, font=FONT_LABEL)
add_weapons_btn = tk.Button(root, text="Add Weapons", command=select_folder_and_add_weapons, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=FONT_LABEL)
add_vehicles_btn = tk.Button(root, text="Add Vehicles", command=select_folder_and_add_vehicles, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=FONT_LABEL)

update_buttons()

# Update buttons when framework changes
selected_framework.trace("w", lambda *args: update_buttons())

root.mainloop()
