import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Easy Sudoku Solver")

        self.board = [[0 for _ in range(9)] for _ in range(9)]  # 9x9 board
        self.cells = [[None for _ in range(9)] for _ in range(9)]  # UI cells
        self.fixed_cells = set()  # (r, c) positions of fixed cells
        self.create_grid()

        button_frame = tk.Frame(master)
        button_frame.grid(row=9, column=0, columnspan=9, pady=10)

        self.solve_button = tk.Button(button_frame, text="Solve Sudoku", command=self.solve_sudoku)
        self.solve_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(button_frame, text="Clear Grid", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT, padx=10)

    def create_grid(self):
        """Create a 9x9 grid of Entry widgets."""
        for r in range(9):
            for c in range(9):
                entry = tk.Entry(self.master, width=2, font=('Arial', 20),
                                 justify="center", borderwidth=1, relief="solid")
                entry.grid(row=r, column=c, padx=2, pady=2)
                self.cells[r][c] = entry

    def update_board(self):
        """Update internal board and fixed cells based on entries."""
        self.fixed_cells.clear()
        for r in range(9):
            for c in range(9):
                value = self.cells[r][c].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    self.board[r][c] = int(value)
                    self.fixed_cells.add((r, c))
                    self.cells[r][c].config(bg="#DDDDDD")  # Gray for fixed cells
                else:
                    self.board[r][c] = 0
                    self.cells[r][c].config(bg="white")  # White for empty

    def solve_sudoku(self):
        """Solve the Sudoku puzzle."""
        self.update_board()
        if self.solve():
            self.update_grid()
            messagebox.showinfo("Success", "Sudoku Solved!")
        else:
            messagebox.showerror("Error", "No solution exists!")

    def solve(self):
        """Backtracking algorithm."""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    for num in range(1, 10):
                        if self.is_valid(r, c, num):
                            self.board[r][c] = num
                            if self.solve():
                                return True
                            self.board[r][c] = 0  # Backtrack
                    return False
        return True

    def is_valid(self, r, c, num):
        """Check if num can be placed at board[r][c]."""
        # Check row and column
        for i in range(9):
            if self.board[r][i] == num or self.board[i][c] == num:
                return False

        # Check 3x3 block
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def update_grid(self):
        """Update UI with solved board."""
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                if self.board[r][c] != 0:
                    self.cells[r][c].insert(tk.END, str(self.board[r][c]))
                # Keep fixed cells gray
                if (r, c) in self.fixed_cells:
                    self.cells[r][c].config(bg="#DDDDDD")
                else:
                    self.cells[r][c].config(bg="white")

    def clear_grid(self):
        """Clear the entire grid."""
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(bg="white")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fixed_cells.clear()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
