import tkinter as tk
import sv_ttk

from tkinter import ttk
from app.views.home_view import HomeView


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Unreal Localization Tool")
        self.geometry("1080x600")
        sv_ttk.set_theme("dark")

        # Main container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        self.current_view = HomeView(container)
        self.current_view.pack(fill="both", expand=True)
