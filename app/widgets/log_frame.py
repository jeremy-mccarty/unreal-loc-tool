import tkinter as tk
from tkinter import ttk


class LogFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text="Output Log:").pack(anchor="w")
        self.log_text_area = tk.Text(self, wrap="word", state="disabled")
        self.log_text_area.pack(anchor="w", fill="both")

    def log(self, message):
        self.log_text_area.configure(state="normal")
        self.log_text_area.insert(tk.END, message + "\n")
        self.log_text_area.see(tk.END)
        self.log_text_area.configure(state="disabled")
