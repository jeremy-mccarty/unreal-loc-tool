import os
import tkinter as tk
from tkinter import ttk, filedialog
import app.unreal_loc_tool as ult
from app.widgets.target_frame import TargetFrame
from app.widgets.log_frame import LogFrame
from app.ui.layout import form_row


class HomeView(ttk.Frame):

    ROW_TITLE, ROW_FILE, ROW_CONVERT, ROW_FOLDER, ROW_BATCH, ROW_TARGETS, ROW_LOG = (
        range(7)
    )

    TALL = (0, 20)
    SHORT = pady = (0, 10)

    def __init__(self, parent):
        super().__init__(parent, padding=20)

        # ---------------- Title ----------------
        ttk.Label(
            self,
            text="Unreal Localization Tool",
            font=("Segoe UI", 20),
            anchor="w",
            wraplength=600,
        ).grid(row=self.ROW_TITLE, column=0, columnspan=3, sticky="ew", pady=self.SHORT)

        # ---------------- Variables ----------------
        self.file_path = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.targets = []

        # ---------------- File Input Row ----------------
        file_entry = ttk.Entry(self, textvariable=self.file_path)
        file_btn = ttk.Button(self, text="Browse", command=self.select_path)
        form_row(self, self.ROW_FILE, "Input File", file_entry, file_btn)

        # ---------------- Convert Buttons ----------------
        convert_row = ttk.Frame(self)
        convert_row.grid(
            row=self.ROW_CONVERT, column=0, columnspan=3, sticky="ew", pady=(10, 20)
        )
        convert_row.grid_columnconfigure(0, weight=1)
        convert_row.grid_columnconfigure(1, weight=1)

        ttk.Button(convert_row, text="Convert CSV → PO", command=self.convert).grid(
            row=0, column=0, sticky="ew", padx=5
        )
        ttk.Button(
            convert_row, text="Convert PO → CSV", command=lambda: self.convert(False)
        ).grid(row=0, column=1, sticky="ew", padx=5)

        # ---------------- Folder Input Row ----------------
        folder_entry = ttk.Entry(self, textvariable=self.folder_path)
        folder_btn = ttk.Button(self, text="Browse", command=self.select_folder)
        form_row(self, self.ROW_FOLDER, "Folder Path", folder_entry, folder_btn)

        # ---------------- Batch Convert ----------------
        ttk.Button(
            self, text="Batch Convert PO → CSV", command=self.batch_convert
        ).grid(row=self.ROW_BATCH, column=0, columnspan=3, sticky="ew", pady=self.TALL)

        # ---------------- Target Frame ----------------
        self.target_frame = TargetFrame(self)
        self.target_frame.grid(
            row=self.ROW_TARGETS, column=0, columnspan=3, sticky="nsew", pady=self.SHORT
        )

        # ---------------- Log Frame ----------------
        self.log_frame = LogFrame(self)
        self.log_frame.grid(row=self.ROW_LOG, column=0, columnspan=3, sticky="nsew")

        # ---------------- Grid weights ----------------
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(self.ROW_TARGETS, weight=0)
        self.grid_rowconfigure(self.ROW_LOG, weight=1)

    # ---------------- Actions ----------------
    def convert(self, csv_to_po=True):
        file_path = self.file_path.get()
        if not file_path:
            self.log_frame.log("No file selected")
            return

        result = ult.csv_to_po(file_path) if csv_to_po else ult.po_to_csv(file_path)
        self.log_frame.log(result)

    def batch_convert(self, csv_to_po=True):
        folder_path = self.folder_path.get()
        if not folder_path:
            self.log_frame.log("No folder selected")
            return

        result = ult.batch_convert_recursive(
            folder_path, self.target_frame.get_selected_targets()
        )
        self.log_frame.log(result)

    def select_path(self):
        file_path = filedialog.askopenfilename(
            title="Select input file",
            filetypes=[("CSV files", "*.csv"), ("PO files", "*.po")],
        )
        if file_path:
            self.file_path.set(file_path)
            self.log_frame.log(f"Set file path: {file_path}")

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select folder")
        if folder_path:
            targets = [
                os.path.join(root, f)
                for root, _, files in os.walk(folder_path)
                for f in files
                if f.endswith(".po")
            ]
            self.target_frame.fill_targets(targets)
            self.folder_path.set(folder_path)
            self.log_frame.log(f"Set folder path: {folder_path}")
