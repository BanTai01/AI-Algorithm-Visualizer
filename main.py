import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Function to open other Python files
def open_module(filename):
    try:
        subprocess.Popen(["python", filename])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open {filename}\n{e}")

# Create main window
root = tk.Tk()
root.title("AI Project - Main Menu")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

tk.Label(root, text=" AI Algorithm Visualizer", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)

modules = [
    ("Search Algorithm Visualizer", "search_visualizer.py"),
    ("Tic-Tac-Toe with Minimax", "tictactoe.py"),
    ("Sudoku Solver", "sudoku_solver.py"),
    ("Rule-based System", "rule_based_system.py"),
    ("Fuzzy Logic System", "fuzzy_logic.py")
]

for text, file in modules:
    tk.Button(
        root, text=text, width=30, height=2,
        command=lambda f=file: open_module(f),
        bg="#007acc", fg="white", font=("Helvetica", 10, "bold")
    ).pack(pady=10)

root.mainloop()
