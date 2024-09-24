import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sv_ttk  # Import the sv_ttk module for Sun-Valley theme

# Global variable to store the selected file path
selected_file_path = None

# Function to apply the Sun-Valley theme to Tkinter
def set_theme(root):
    try:
        sv_ttk.set_theme("dark")  # Set the theme to dark
    except Exception as e:
        messagebox.showerror("Theme Error", f"Could not apply theme: {e}")

# Function to open file explorer and select a Lua script
def select_file():
    global selected_file_path  # Use the global variable to store the file path
    selected_file_path = filedialog.askopenfilename(
        title="Select QBCore Lua Script",
        filetypes=[("Lua Files", "*.lua")],
    )
    if selected_file_path:
        file_label.config(text=f"Selected file: {os.path.basename(selected_file_path)}")
        convert_button.config(state="normal")  # Enable Convert button after selection
    else:
        messagebox.showwarning("No file selected", "Please select a Lua script file.")

# Function to convert QBCore Lua script to QBox equivalent
def convert_qbcore_to_qbox():
    if not selected_file_path:  # Check if a file has been selected
        messagebox.showwarning("No file selected", "Please select a Lua script file first.")
        return

    # Read the Lua file
    with open(selected_file_path, "r") as file:
        code = file.read()

    # Define replacements (QBCore to QBox conversions)
    replacements = [
        (r"QBCore\.Functions\.GetPlayerData\(\)", "QBX.PlayerData"),
        (r"QBCore\.Functions\.GetPlate\((\w+)\)", r"qbx.getVehiclePlate(\1)"),
        (r"QBCore\.Shared\.Jobs", "exports.qbx_core:GetJobs()"),
        (r"QBCore\.Shared\.Gangs", "exports.qbx_core:GetGangs()"),
        (r"QBCore\.Shared\.Vehicles", "exports.qbx_core:GetVehiclesByName()"),
        (r"QBCore\.Shared\.Weapons", "exports.qbx_core:GetWeapons()"),
        (r"QBCore\.Shared\.Locations", "exports.qbx_core:GetLocations()"),
        (r"QBCore\.Shared\.Items", "exports.ox_inventory:Items()"),
        (r"exports\['qb%-core'\]:KeyPressed\(\)", "lib.hideTextUI()"),
        (r"exports\['qb%-core'\]:HideText\(\)", "lib.hideTextUI()"),
        (r"exports\['qb%-core'\]:DrawText\((\w+), (\w+)\)", r"lib.showTextUI(\1, { position = \2 })"),
        (r"exports\['qb%-core'\]:ChangeText\((\w+), (\w+)\)", r"lib.hideTextUI() lib.showTextUI(\1, { position = \2 })")
    ]

    # Apply replacements
    for pattern, replacement in replacements:
        code = re.sub(pattern, replacement, code)

    # Save the converted Lua file
    output_file = selected_file_path.replace(".lua", "_converted.lua")
    with open(output_file, "w") as file:
        file.write(code)

    messagebox.showinfo("Conversion Complete", f"File saved as: {output_file}")

# Set up the main application window
root = tk.Tk()
root.title("QBCore to QBox Converter")
root.geometry("400x200")

# Apply Sun-Valley theme
set_theme(root)

# Create and configure widgets
file_label = ttk.Label(root, text="No file selected", anchor="center")
file_label.pack(pady=20)

select_button = ttk.Button(root, text="Select Lua Script", command=select_file)
select_button.pack(pady=10)

convert_button = ttk.Button(root, text="Convert to QBox", command=convert_qbcore_to_qbox, state="disabled")
convert_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
