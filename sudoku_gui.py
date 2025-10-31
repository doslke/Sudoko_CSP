import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import time
from sudoku_solver import SudokuSolver

class SudokuGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku SOLVER!")
        self.window.geometry("445x650")
        self.entries = []


        self.stats_label = tk.Label(self.window, text="", font=("Arial", 12))
        self.stats_label.grid(row=10, column=0, columnspan=9, pady=5)


        self.log_text = tk.Text(self.window, height=8, width=50)
        self.log_text.grid(row=11, column=0, columnspan=9, pady=5)

    def show_stats(self, steps, elapsed):
        self.stats_label.config(text=f"Steps/Backtracks: {steps}")

    def log_step(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.window.update()

    def create_grid(self):
        vcmd = (self.window.register(self.validate_input), "%P", "%W")
        for i in range(9):
            row_entries = []
            for j in range(9):
                e = tk.Entry(
                    self.window,
                    width=3,
                    font=("Arial", 18),
                    justify="center",
                    validate="key",
                    validatecommand=vcmd
                )
                e.grid(row=i, column=j, padx=3, pady=3)
                row_entries.append(e)
            self.entries.append(row_entries)

    def validate_input(self, new_value, widget_name):
        if new_value == "":
            return True
        if len(new_value) == 1 and new_value.isdigit() and 0 <= int(new_value) <= 9:
            return True
        widget = self.window.nametowidget(widget_name)
        self.window.after(10, lambda: widget.delete(0, tk.END))
        messagebox.showerror("INPUT ERROR", "ONLY CAN INPUT NUMBER BETWEEN 0 AND 9!")
        return False

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == '':
                    val = 0
                row.append(int(val))
            grid.append(row)
        return grid

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg="white")
        self.log_text.delete(1.0, tk.END)
        self.stats_label.config(text="")

    def create_buttons(self):
        tk.Button(self.window, text="SOLVE!", command=self.solve_button).grid(row=9, column=2, columnspan=2, pady=5)
        tk.Button(self.window, text="CLEAR", command=self.clear_grid).grid(row=9, column=5, columnspan=2, pady=5)
        tk.Button(self.window, text="LOAD", command=self.load_file).grid(row=9, column=0, columnspan=2, pady=5)

    def solve_button(self):
        grid = self.get_grid()
        solver = SudokuSolver(grid, self)
        try:
            start = time.time()
            solver.runs()
            end = time.time()
            # 可在 solver 内记录 steps/backtracks 并传回 gui
            self.show_stats(getattr(solver, "steps", 0), end - start)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e1:
            messagebox.showerror("Error", str(e1))

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Sudoku file",
            filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if not file_path:
            return
        try:
            grid = self.read_grid_from_file(file_path)
            self.update_grid(grid)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def read_grid_from_file(self, file_path):
        grid = []
        if file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    row = [int(val) if val != '' else 0 for val in line.split()]
                    if len(row) != 9:
                        raise ValueError("Each row must have 9 numbers")
                    grid.append(row)
        elif file_path.endswith(".csv"):
            with open(file_path, "r", newline='') as f:
                reader = csv.reader(f)
                for row_vals in reader:
                    if not row_vals:
                        continue
                    row = [int(val.strip()) if val.strip() != '' else 0 for val in row_vals]
                    if len(row) != 9:
                        raise ValueError("Each row must have 9 numbers")
                    grid.append(row)
        else:
            raise ValueError("Unsupported file format")
        if len(grid) != 9:
            raise ValueError("The grid must have 9 rows")
        return grid

    def update_grid(self, grid, highlight=None):
        for i in range(9):
            for j in range(9):
                val = grid[i][j]
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                if val != 0:
                    entry.insert(0, str(val))
                entry.config(bg="yellow" if highlight == (i, j) else "white")
        self.window.update()

    def run(self):
        self.create_grid()
        self.create_buttons()
        self.window.mainloop()



if __name__ == "__main__":
    gui = SudokuGUI()
    gui.run()
