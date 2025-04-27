import tkinter as tk
from tkinter import messagebox
import skfuzzy as fuzz
import numpy as np
import random

# Main GUI Window
root = tk.Tk()
root.title("Fuzzy Logic System")
root.geometry("500x400")
root.configure(bg="#f9f9f9")

# Menu logic handler
def show_menu(selection):
    # Remove all widgets except the menu
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()

    if selection == "Food Suggestion":
        show_food_suggestion()

# Food Suggestion System
def show_food_suggestion():
    title = tk.Label(root, text="Fuzzy Food Suggestion", font=("Helvetica", 14, "bold"), bg="#f9f9f9")
    title.pack(pady=10)

    tk.Label(root, text="Hunger Level (0-10)", bg="#f9f9f9").pack()
    hunger_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    hunger_scale.pack()

    tk.Label(root, text="Spicy Preference (0-10)", bg="#f9f9f9").pack()
    spicy_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    spicy_scale.pack()

    def suggest_food():
        hunger = hunger_scale.get()
        spice = spicy_scale.get()

        # Defining fuzzy sets for hunger and spice preferences
        x = np.arange(0, 11, 1)  # Fuzzy range from 0 to 10
        hunger_high = fuzz.trimf(x, [5, 10, 10])  # High hunger membership function
        spice_high = fuzz.trimf(x, [5, 10, 10])   # High spice membership function

        # Evaluating fuzzy values for hunger and spice
        h_val = fuzz.interp_membership(x, hunger_high, hunger)  # Membership for hunger
        s_val = fuzz.interp_membership(x, spice_high, spice)    # Membership for spice

        # Defining food options
        heavy_spicy_food = ["Biriyani", "Kacchi", "Spicy Chicken Curry"]
        heavy_mild_food = ["Rice with Curry", "Khichuri", "Fried Rice with Egg"]
        spicy_snacks = ["Fuchka", "Chatpati", "Jhalmuri", "Spicy Samosa"]
        light_snacks = ["Sandwich", "Rolls", "Biscuits", "Cookies"]

        # Decision-making for food suggestion
        if h_val > 0.7 and s_val > 0.7:
            food = random.choice(heavy_spicy_food)
            msg = f"🔥 Suggestion: {food}"
        elif h_val > 0.7:
            food = random.choice(heavy_mild_food)
            msg = f"🍛 Suggestion: {food}"
        elif s_val > 0.7:
            food = random.choice(spicy_snacks)
            msg = f"🌶️ Suggestion: {food}"
        else:
            food = random.choice(light_snacks)
            msg = f"🍪 Suggestion: {food}"

        messagebox.showinfo("Food Suggestion", msg)

    tk.Button(root, text="Get Suggestion", command=suggest_food, bg="#007acc", fg="white").pack(pady=10)

# Create a menu for navigation
menu_bar = tk.Menu(root)
option_menu = tk.Menu(menu_bar, tearoff=0)
option_menu.add_command(label="Food Suggestion", command=lambda: show_menu("Food Suggestion"))
menu_bar.add_cascade(label="Select System", menu=option_menu)
root.config(menu=menu_bar)

# Initial view
show_menu("Food Suggestion")

root.mainloop()
