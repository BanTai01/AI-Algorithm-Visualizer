import tkinter as tk
from tkinter import messagebox
import time
from queue import Queue, LifoQueue, PriorityQueue
from itertools import count

GRID_SIZE = 20
CELL_SIZE = 30

class Cell:
    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button
        self.state = "empty"  # empty, wall, start, end, visited, path

class SearchVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Search Algorithm Visualizer")
        self.grid = []
        self.start = None
        self.end = None
        self.build_grid()

        self.selected_algorithm = None

        algo_frame = tk.Frame(master)
        algo_frame.pack(pady=10)

        self.bfs_button = tk.Button(algo_frame, text="BFS", command=self.run_bfs)
        self.bfs_button.pack(side=tk.LEFT, padx=10)

        self.dfs_button = tk.Button(algo_frame, text="DFS", command=self.run_dfs)
        self.dfs_button.pack(side=tk.LEFT, padx=10)

        self.astar_button = tk.Button(algo_frame, text="A*", command=self.run_astar)
        self.astar_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_grid)
        self.reset_button.pack(pady=10)

    def build_grid(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                btn = tk.Button(self.frame, width=2, height=1, bg="white",
                                command=lambda x=i, y=j: self.cell_clicked(x, y))
                btn.grid(row=i, column=j)
                row.append(Cell(i, j, btn))
            self.grid.append(row)

    def cell_clicked(self, x, y):
        cell = self.grid[x][y]
        if not self.start:
            cell.state = "start"
            cell.button.config(bg="green")
            self.start = cell
        elif not self.end and cell != self.start:
            cell.state = "end"
            cell.button.config(bg="red")
            self.end = cell
        elif cell.state == "empty":
            cell.state = "wall"
            cell.button.config(bg="black")

    def reset_grid(self):
        # Reset cells
        for row in self.grid:
            for cell in row:
                cell.state = "empty"
                cell.button.config(bg="white")

        # Reset variables
        self.start = None
        self.end = None

        # Reset button colors
        self.bfs_button.config(bg="SystemButtonFace")
        self.dfs_button.config(bg="SystemButtonFace")
        self.astar_button.config(bg="SystemButtonFace")

    def highlight_button(self, selected_button):
        # Reset all buttons first
        self.bfs_button.config(bg="SystemButtonFace")
        self.dfs_button.config(bg="SystemButtonFace")
        self.astar_button.config(bg="SystemButtonFace")

        # Highlight the selected button
        selected_button.config(bg="skyblue")

    def run_bfs(self):
        self.highlight_button(self.bfs_button)
        self._run_search(Queue())

    def run_dfs(self):
        self.highlight_button(self.dfs_button)
        self._run_search(LifoQueue())

    def run_astar(self):
        self.highlight_button(self.astar_button)
        self._run_astar()

    def _run_search(self, structure):
        if not self.start or not self.end:
            messagebox.showwarning("Warning", "Please select a start and end point.")
            return

        self.clear_path()

        structure.put((self.start, []))
        visited = set()
        visited.add((self.start.x, self.start.y))

        while not structure.empty():
            current, path = structure.get()

            if current == self.end:
                for cell in path:
                    if cell not in [self.start, self.end]:
                        cell.state = "path"
                        cell.button.config(bg="yellow")
                return

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    neighbor = self.grid[nx][ny]
                    if neighbor.state in ["empty", "end"] and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        if neighbor != self.end:
                            neighbor.state = "visited"
                            neighbor.button.config(bg="blue")
                        structure.put((neighbor, path + [current]))
                        self.master.update()
                        time.sleep(0.01)

        messagebox.showinfo("Result", "No path found!")

    def _run_astar(self):
        if not self.start or not self.end:
            messagebox.showwarning("Warning", "Please select a start and end point.")
            return

        self.clear_path()

        def heuristic(a, b):
            return abs(a.x - b.x) + abs(a.y - b.y)

        counter = count()
        open_set = PriorityQueue()
        open_set.put((0, next(counter), self.start, []))
        g_score = {(self.start.x, self.start.y): 0}
        visited = set()

        while not open_set.empty():
            _, _, current, path = open_set.get()

            if current == self.end:
                for cell in path:
                    if cell not in [self.start, self.end]:
                        cell.state = "path"
                        cell.button.config(bg="yellow")
                return

            visited.add((current.x, current.y))

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    neighbor = self.grid[nx][ny]
                    if neighbor.state != "wall" and (nx, ny) not in visited:
                        temp_g = g_score[(current.x, current.y)] + 1
                        if (nx, ny) not in g_score or temp_g < g_score[(nx, ny)]:
                            g_score[(nx, ny)] = temp_g
                            f_score = temp_g + heuristic(neighbor, self.end)
                            open_set.put((f_score, next(counter), neighbor, path + [current]))
                            if neighbor.state != "end":
                                neighbor.state = "visited"
                                neighbor.button.config(bg="blue")
                            self.master.update()
                            time.sleep(0.01)

        messagebox.showinfo("Result", "No path found!")

    def clear_path(self):
        for row in self.grid:
            for cell in row:
                if cell.state in ["visited", "path"]:
                    cell.state = "empty"
                    cell.button.config(bg="white")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchVisualizer(root)
    root.mainloop()
