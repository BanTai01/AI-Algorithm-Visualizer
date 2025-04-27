import tkinter as tk
from tkinter import messagebox
import skfuzzy as fuzz
import numpy as np

# Main GUI Window
root = tk.Tk()
root.title("Advanced Fuzzy Food Suggestion System")
root.geometry("600x500")
root.configure(bg="#f9f9f9")

def show_menu(selection):
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()

    if selection == "Food Suggestion":
        show_food_suggestion()

def show_food_suggestion():
    title = tk.Label(root, text="🍽️ Rule Based Food Suggestion", font=("Helvetica", 16, "bold"), bg="#f9f9f9")
    title.pack(pady=10)

    # Hunger Level
    tk.Label(root, text="Hunger Level (0-10)", bg="#f9f9f9").pack()
    hunger_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    hunger_scale.pack()

    # Spicy Preference
    tk.Label(root, text="Spicy Preference (0-10)", bg="#f9f9f9").pack()
    spicy_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    spicy_scale.pack()

    # Mood
    tk.Label(root, text="Mood Level (0-10)", bg="#f9f9f9").pack()
    mood_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    mood_scale.pack()

    # Weather preference
    tk.Label(root, text="Weather Preference (0-10)", bg="#f9f9f9").pack()
    weather_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    weather_scale.pack()

    def suggest_food():
        hunger = hunger_scale.get()
        spice = spicy_scale.get()
        mood = mood_scale.get()
        weather = weather_scale.get()

        x = np.arange(0, 11, 1)

        hunger_high = fuzz.trimf(x, [5, 10, 10])
        spice_high = fuzz.trimf(x, [5, 10, 10])
        mood_happy = fuzz.trimf(x, [5, 10, 10])
        weather_hot = fuzz.trimf(x, [5, 10, 10])

        h_val = fuzz.interp_membership(x, hunger_high, hunger)
        s_val = fuzz.interp_membership(x, spice_high, spice)
        m_val = fuzz.interp_membership(x, mood_happy, mood)
        w_val = fuzz.interp_membership(x, weather_hot, weather)

        suggestion = ""

        if h_val > 0.7 and s_val > 0.7:
            suggestion = "🔥 Heavy & Spicy: Biriyani, Kacchi, Spicy Kebabs"
        elif h_val > 0.7 and s_val <= 0.7:
            suggestion = "🍛 Heavy & Mild: Rice with Butter Chicken, Pasta Alfredo"
        elif h_val <= 0.7 and s_val > 0.7:
            suggestion = "🌶️ Light & Spicy: Fuchka, Chatpati, Tacos"
        else:
            suggestion = "🍪 Light Snacks: Sandwich, Burger, Noodles, French Fries"

        # Mood-based dessert
        if m_val > 0.7:
            suggestion += "\n🎂 Bonus: Try some Ice Cream, Cake, or Brownies!"

        # Weather-based drink
        if w_val > 0.7:
            suggestion += "\n🥤 Cool Drink: Lemonade, Iced Coffee, Milkshake."
        else:
            suggestion += "\n☕ Warm Drink: Tea, Hot Chocolate, Soup."

        messagebox.showinfo("Food Suggestion", suggestion)

    tk.Button(root, text="Get Food Suggestion", command=suggest_food, bg="#007acc", fg="white", font=("Helvetica", 12)).pack(pady=20)

# Create a menu
menu_bar = tk.Menu(root)
option_menu = tk.Menu(menu_bar, tearoff=0)
option_menu.add_command(label="Food Suggestion", command=lambda: show_menu("Food Suggestion"))
menu_bar.add_cascade(label="Select System", menu=option_menu)
root.config(menu=menu_bar)

# Initial view
show_menu("Food Suggestion")

root.mainloop()
