import tkinter as tk
import app.unreal_loc_tool as ult

from tkinter import ttk, filedialog


class HomeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        # Configure main grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Shared padding vars
        short_padding = (0, 10)
        tall_padding = (0, 20)
        left_padding = (10, 0)

        # ---------------- Title ----------------
        ttk.Label(
            self,
            text="Unreal Localization Tool",
            font=("Segoe UI", 20),
            anchor="w",
            wraplength=600,  # Wrap if window narrows
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=short_padding)

        # ---------------- File Path ----------------
        self.file_path = tk.StringVar()
        ttk.Button(
            self,
            text="Select Input Path",
            command=self.select_path,
        ).grid(row=2, column=0, sticky="ew", pady=short_padding)

        # Entry showing the path
        ttk.Entry(self, textvariable=self.file_path).grid(
            row=2, column=1, sticky="ew", padx=left_padding, pady=short_padding
        )

        # ---------------- Convert Buttons ----------------
        ttk.Button(self, text="Convert CSV → PO", command=lambda: (self.convert)).grid(
            row=3, column=0, sticky="ew", pady=tall_padding
        )
        ttk.Button(
            self, text="Convert PO → CSV", command=lambda: (self.convert(False))
        ).grid(row=3, column=1, sticky="ew", pady=tall_padding, padx=left_padding)

        # ---------------- Output log ----------------
        ttk.Label(self, text="Output Log:").grid(row=4, column=0, sticky="w")
        self.log_text_area = tk.Text(self, wrap="word", state="disabled")
        self.log_text_area.grid(row=5, column=0, columnspan=2, sticky="nsew")

    def convert(self, csv_to_po=True):
        file_path = self.file_path.get()
        if not file_path:
            self.log("No file selected")
            return

        if csv_to_po:
            result = ult.csv_to_po(file_path)
        else:
            result = ult.po_to_csv(file_path)

        self.log(result)

    def select_path(self):
        file_path = filedialog.askopenfilename(
            title=f"Select input file",
            filetypes=[("CSV files", "*.csv"), ("PO files", "*.po")],
        )

        if not file_path:
            self.log("No file selected")
            return

        self.file_path.set(file_path)
        self.log(f"Set file path: {file_path}")

    def log(self, message):
        self.log_text_area.configure(state="normal")
        self.log_text_area.insert(tk.END, message + "\n")
        self.log_text_area.see(tk.END)
        self.log_text_area.configure(state="disabled")
