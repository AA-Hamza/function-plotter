import tkinter as tk
from tkinter import messagebox
import expression
import matplotlib.pyplot as plt


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.initialize_layout()

    def initialize_layout(self):
        self.grid(padx=20)
        self.function_label = tk.Label(text="Function: ")
        self.function_label.grid(padx=5, row=0, column=0, sticky="w")

        self.function_entry = tk.Entry()
        self.function_entry.insert(tk.END,"x*x")
        self.function_entry.grid(padx=10, row=0, column=1, sticky="ew")

        self.min_label = tk.Label(text="Min: ")
        self.min_label.grid(padx=5, row=1, column=0, sticky="w")

        self.min_entry = tk.Entry()
        self.min_entry.grid(padx=10, row=1, column=1, columnspan=2, sticky="ew")
        self.min_entry.insert(tk.END,"-200")

        self.max_label = tk.Label(text="Max: ")
        self.max_label.grid(padx=5, row=2, column=0, sticky="w")

        self.max_entry = tk.Entry()
        self.max_entry.grid(padx=10, row=2, column=1, columnspan=2, sticky="ew")
        self.max_entry.insert(tk.END,"200")

        self.plot_button = tk.Button(text="Plot", command=self.plot_button_handler)
        self.plot_button.grid(row=3, column=0, columnspan=3)

    
    def validate_min_max(self, min, max):
        try:
            min = float(min)
            max = float(max)
        except:
            raise Exception("Invalid Min/Max Value")
        if min >= max:
            raise Exception("Min should be smaller than Max")
        return min, max

    def plot_button_handler(self):
        try:
            equation_str = self.function_entry.get().lower()
            min, max = self.validate_min_max(self.min_entry.get(), self.max_entry.get())
            self.equation_solver = expression.Expression(equation_str, min, max)
            self.plot()
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def plot(self):
        plt.plot(self.equation_solver.eval_expression())
        plt.show()


root = tk.Tk()
root.title("Function Plotter")
root.geometry("300x120")
root.resizable(width=False, height=False)
root.iconphoto(True, tk.PhotoImage(file="icon.png"))
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
myapp = App(root)

myapp.mainloop()
