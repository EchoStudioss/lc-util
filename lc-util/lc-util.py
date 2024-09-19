import os
import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Define output files
ITEMS_OUTPUT_FILE = "ox_inventory_items.txt"
VEHICLES_OUTPUT_FILE = "qb_vehicles.txt"

# Colors and styles
BACKGROUND_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
TEXT_COLOR = "#ecf0f1"
FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 12)

# Hover effect functions
def on_enter(event):
    event.widget['background'] = '#2980b9'
    
def on_leave(event):
    event.widget['background'] = BUTTON_COLOR

# Function to add items from PNG images in a folder
def add_items_from_images(folder_path):
    items = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):
            item_name = os.path.splitext(file_name)[0]  # Remove .png extension
            item_label = item_name.capitalize()  # Capitalize item name for label
            item_weight = 100  # Default weight, can be customized
            items.append({
                "name": item_name,
                "label": item_label,
                "weight": item_weight,
                "stack": True,
                "close": True
            })
    return items

# Function to add items from a notepad (txt) file
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

# Function to add items from a CSV file
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

# Function to save items in the required format to a text file
def save_items_to_text_file(items):
    with open(ITEMS_OUTPUT_FILE, 'w') as file:
        for item in items:
            item_entry = (
                f"['{item['name']}'] = {{\n"
                f"    label = '{item['label']}',\n"
                f"    weight = {item['weight']},\n"
                f"    stack = true,\n"
                f"    close = true,\n"
                f"}},\n"
            )
            file.write(item_entry)
    messagebox.showinfo("Success", f"Items saved to {ITEMS_OUTPUT_FILE}")

# Function to handle adding items based on user choice
def add_items(choice):
    items = []
    
    if choice == 'images':
        folder_path = filedialog.askdirectory(title="Select Folder with PNG Images")
        if folder_path:
            items = add_items_from_images(folder_path)
        else:
            messagebox.showerror("Error", "No folder selected.")
    elif choice == 'notepad':
        file_path = filedialog.askopenfilename(title="Select Notepad File", filetypes=[("Text files", "*.txt")])
        if file_path:
            items = add_items_from_notepad(file_path)
        else:
            messagebox.showerror("Error", "No file selected.")
    elif choice == 'csv':
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            items = add_items_from_csv(file_path)
        else:
            messagebox.showerror("Error", "No file selected.")

    if items:
        save_items_to_text_file(items)
    else:
        messagebox.showwarning("No Items", "No items found to add.")

# Recursive function to search vehicle models from meta files
def add_vehicles_from_meta_recursive(folder_path):
    vehicles = []
    model_name_pattern = re.compile(r'<modelName>(\w+)</modelName>')  # Pattern to extract model names

    for root, dirs, files in os.walk(folder_path):  # Recursively walk through all directories
        for file_name in files:
            if file_name == 'vehicles.meta':  # Look for the vehicles.meta file
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()  # Read the file content
                    matches = model_name_pattern.findall(content)  # Find all model names

                    for match in matches:
                        vehicle_entry = {
                            "model": match.lower(),
                            "name": match.capitalize(),
                            "brand": "Unknown",
                            "price": 20000,
                            "category": "unknown",
                            "type": "automobile",
                            "shop": "pdm"
                        }
                        vehicles.append(vehicle_entry)
    return vehicles

# Function to save vehicles to a text file
def save_vehicles_to_text_file(vehicles):
    with open(VEHICLES_OUTPUT_FILE, 'w') as file:
        for vehicle in vehicles:
            vehicle_entry = (f"{{ model = '{vehicle['model']}', name = '{vehicle['name']}', "
                             f"brand = '{vehicle['brand']}', price = {vehicle['price']}, "
                             f"category = '{vehicle['category']}', type = '{vehicle['type']}', "
                             f"shop = '{vehicle['shop']}' }},\n")
            file.write(vehicle_entry)
    messagebox.showinfo("Success", f"Vehicles saved to {VEHICLES_OUTPUT_FILE}")

# GUI to get folder path for vehicles
def select_folder_and_add_vehicles():
    folder_path = filedialog.askdirectory()  # Open folder dialog
    if folder_path:
        vehicles = add_vehicles_from_meta_recursive(folder_path)
        if vehicles:
            save_vehicles_to_text_file(vehicles)
        else:
            messagebox.showwarning("No Vehicles", "No vehicles found in the meta files.")
    else:
        messagebox.showerror("Error", "No folder selected.")

# GUI setup for adding items
def add_items_window():
    item_window = tk.Toplevel()
    item_window.title("Add Items")
    item_window.configure(bg=BACKGROUND_COLOR)

    frame = tk.Frame(item_window, bg=BACKGROUND_COLOR)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Choose how you'd like to add items:", font=FONT_LABEL, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_COLOR, 'fg': 'white', 'font': FONT_LABEL, 'bd': 0, 'relief': 'flat'}
    btn_images = tk.Button(frame, text="From PNG Images in a Folder", command=lambda: add_items('images'), **button_style)
    btn_images.pack(pady=5, fill=tk.X)

    btn_notepad = tk.Button(frame, text="From Notepad File", command=lambda: add_items('notepad'), **button_style)
    btn_notepad.pack(pady=5, fill=tk.X)

    btn_csv = tk.Button(frame, text="From CSV File", command=lambda: add_items('csv'), **button_style)
    btn_csv.pack(pady=5, fill=tk.X)

    btn_close = tk.Button(frame, text="Close", command=item_window.destroy, **button_style)
    btn_close.pack(pady=10, fill=tk.X)

# Main GUI setup
def main_gui():
    global root
    root = tk.Tk()
    root.title("Vehicle & Item Manager")
    root.configure(bg=BACKGROUND_COLOR)
    root.geometry("400x300")
    root.resizable(True, True)

    frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Welcome to the Vehicle & Item Manager", font=FONT_TITLE, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_COLOR, 'fg': 'white', 'font': FONT_LABEL, 'bd': 0, 'relief': 'flat'}

    btn_images = tk.Button(frame, text="Add Items (Ox Inventory)", command=add_items_window, **button_style)
    btn_images.pack(pady=10, fill=tk.X)
    btn_images.bind("<Enter>", on_enter)
    btn_images.bind("<Leave>", on_leave)

    btn_vehicles = tk.Button(frame, text="Add Vehicles (QB-Core)", command=select_folder_and_add_vehicles, **button_style)
    btn_vehicles.pack(pady=10, fill=tk.X)
    btn_vehicles.bind("<Enter>", on_enter)
    btn_vehicles.bind("<Leave>", on_leave)

    btn_exit = tk.Button(frame, text="Exit", command=root.quit, **button_style)
    btn_exit.pack(pady=10, fill=tk.X)
    btn_exit.bind("<Enter>", on_enter)
    btn_exit.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    main_gui()  # Call the main_gui function to start the GUI

