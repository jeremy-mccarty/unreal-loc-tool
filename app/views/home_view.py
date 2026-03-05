import tkinter as tk
import app.unreal_loc_tool as ult
import os

from tkinter import ttk, filedialog


class HomeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        # Configure main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(8, weight=0)
        self.grid_rowconfigure(10, weight=1)

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
        ttk.Button(self, text="Convert CSV → PO", command=self.convert).grid(
            row=3, column=0, sticky="ew", pady=tall_padding
        )
        ttk.Button(
            self, text="Convert PO → CSV", command=lambda: self.convert(False)
        ).grid(row=3, column=1, sticky="ew", pady=tall_padding, padx=left_padding)

        # ---------------- Folder Path ----------------
        self.targets = []
        self.folder_path = tk.StringVar()
        ttk.Button(
            self,
            text="Select Folder Path",
            command=self.select_folder,
        ).grid(row=4, column=0, sticky="ew", pady=short_padding)

        # Entry showing the path
        ttk.Entry(self, textvariable=self.folder_path).grid(
            row=4, column=1, sticky="ew", padx=left_padding, pady=short_padding
        )

        # ---------------- Batch Convert Button ----------------
        ttk.Button(
            self, text="Batch Convert PO → CSV", command=self.batch_convert
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=tall_padding)

        # ---------------- Target Frame ----------------
        self.targets_visible = True
        self.target_vars = {}

        # Header container (row 6 and 7)
        self.targets_header = ttk.Frame(self)
        self.targets_header.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.targets_label = ttk.Label(self.targets_header, text="Targets (0/0)")
        self.targets_label.pack(side="left", padx=(0, 10))
        spacer = ttk.Frame(self.targets_header)
        spacer.pack(side="left", expand=True, fill="x")
        self.select_all_btn = ttk.Button(
            self.targets_header, text="Select All", command=self.select_all_targets, width=10
        )
        self.select_all_btn.pack(side="right", padx=(5, 0))
        self.deselect_all_btn = ttk.Button(
            self.targets_header, text="Deselect All", command=self.deselect_all_targets, width=10
        )
        self.deselect_all_btn.pack(side="right", padx=(5, 0))
        ttk.Separator(self, orient="horizontal").grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=(2, 5)
        )

        # Scrollable collapsible frame (row 8)
        self.target_canvas = tk.Canvas(self, height=100)  # max visible height
        self.target_frame_scroll = ttk.Frame(self.target_canvas)
        self.target_scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.target_canvas.yview
        )
        self.target_canvas.configure(yscrollcommand=self.target_scrollbar.set)

        self.target_canvas.grid(row=8, column=0, columnspan=2, sticky="nsew")
        self.target_scrollbar.grid(row=8, column=2, sticky="ns")

        self.target_canvas.create_window(
            (0, 0), window=self.target_frame_scroll, anchor="nw"
        )

        self.target_frame_scroll.bind(
            "<Configure>",
            lambda e: self.target_canvas.configure(
                scrollregion=self.target_canvas.bbox("all")
            ),
        )

        # ---------------- Output log ----------------
        ttk.Label(self, text="Output Log:").grid(
            row=9, column=0, sticky="w", pady=(20, 0)
        )
        self.log_text_area = tk.Text(self, wrap="word", state="disabled")
        self.log_text_area.grid(row=10, column=0, columnspan=2, sticky="nsew")

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

    def batch_convert(self, csv_to_po=True):
        folder_path = self.folder_path.get()
        if not folder_path:
            self.log("No folder selected")
            return

        result = ult.batch_convert_recursive(folder_path, self.get_selected_targets())

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

    def select_folder(self):
        folder_path = filedialog.askdirectory(title=f"Select folder")

        if not folder_path:
            self.log("No folder selected")
            return

        self.fill_targets(folder_path)

        self.folder_path.set(folder_path)
        self.log(f"Set folder path: {folder_path}")

    def log(self, message):
        self.log_text_area.configure(state="normal")
        self.log_text_area.insert(tk.END, message + "\n")
        self.log_text_area.see(tk.END)
        self.log_text_area.configure(state="disabled")

    def fill_targets(self, folder_path):
        self.targets = []
        self.target_vars.clear()

        # Collect .po files
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".po"):
                    self.targets.append(os.path.join(root, file))

        # Clear old checkboxes
        for widget in self.target_frame_scroll.winfo_children():
            widget.destroy()

        # Populate checkboxes
        for file_path in sorted(self.targets):
            var = tk.BooleanVar(value=False)
            self.target_vars[file_path] = var

            display_name = os.path.splitext(os.path.basename(file_path))[0]

            chk = ttk.Checkbutton(
                self.target_frame_scroll,
                text=display_name,
                variable=var,
                command=self.update_target_count
            )
            chk.pack(anchor="w", fill="x", padx=5, pady=2)

        # Update count badge
        self.update_target_count()
            
    def select_all_targets(self):
        for var in self.target_vars.values():
            var.set(True)
        self.update_target_count()

    def deselect_all_targets(self):
        for var in self.target_vars.values():
            var.set(False)
        self.update_target_count()
            
    def get_selected_targets(self):
        return [fp for fp, var in self.target_vars.items() if var.get()]
    
    def update_target_count(self):
        total = len(self.target_vars)
        selected = sum(var.get() for var in self.target_vars.values())
        self.targets_label.config(text=f"Targets ({selected}/{total})")
