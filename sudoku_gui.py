import tkinter as tk
from tkinter import messagebox

from sudoku_solver import SudokuSolver


class SudokuGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku SOLVER!")
        self.window.geometry("460x400")
        self.entries = []
    def create_grid(self):
        # 注册输入验证函数
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
        if new_value == "":  # 允许删除
            return True
        if len(new_value) == 1 and new_value.isdigit() and 0 <= int(new_value) <= 9:
            return True
        # 非法输入，清除并提示
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

    def create_buttons(self):
        tk.Button(self.window, text="SOLVE!", command=self.solve_button).grid(row=9, column=2, columnspan=2, pady=10)
        tk.Button(self.window, text="CLEAR", command=self.clear_grid).grid(row=9, column=5, columnspan=2, pady=10)

    def solve_button(self):
        grid = self.get_grid()
        solver = SudokuSolver(grid,self)
        try:
            solver.runs()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e1:
            messagebox.showerror("Error", str(e1))

    def run(self):
        self.create_grid()
        self.create_buttons()
        self.window.mainloop()

    def update_grid(self, grid):
        for i in range(9):
            for j in range(9):
                val = grid[i][j]
                self.entries[i][j].delete(0, tk.END)
                if val != 0:
                    self.entries[i][j].insert(0, str(val))
        self.window.update()


if __name__ == "__main__":
    gui = SudokuGUI()
    gui.run()

