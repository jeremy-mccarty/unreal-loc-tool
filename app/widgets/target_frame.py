import tkinter as tk
from tkinter import ttk


class TargetFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.targets = []
        self.target_vars = {}

        # Header
        self.targets_header = ttk.Frame(self)
        self.targets_header.pack(fill="x", pady=(10, 0))

        self.targets_label = ttk.Label(self.targets_header, text="Targets (0/0)")
        self.targets_label.pack(side="left", padx=(0, 10))

        spacer = ttk.Frame(self.targets_header)
        spacer.pack(side="left", expand=True, fill="x")

        self.select_all_btn = ttk.Button(
            self.targets_header,
            text="Select All",
            command=self.select_all_targets,
            width=10,
        )
        self.select_all_btn.pack(side="right", padx=(5, 0))

        self.deselect_all_btn = ttk.Button(
            self.targets_header,
            text="Deselect All",
            command=self.deselect_all_targets,
            width=10,
        )
        self.deselect_all_btn.pack(side="right", padx=(5, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=(2, 5))

        # Scrollable area
        self.target_canvas = tk.Canvas(self, height=100)
        self.target_frame_scroll = ttk.Frame(self.target_canvas)

        self.target_scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.target_canvas.yview
        )

        self.target_canvas.configure(yscrollcommand=self.target_scrollbar.set)

        self.target_canvas.pack(side="left", fill="both", expand=True)
        self.target_scrollbar.pack(side="right", fill="y")

        self.target_canvas.create_window(
            (0, 0), window=self.target_frame_scroll, anchor="nw"
        )

        self.target_frame_scroll.bind(
            "<Configure>",
            lambda e: self.target_canvas.configure(
                scrollregion=self.target_canvas.bbox("all")
            ),
        )

    def fill_targets(self, targets):
        """Populate checkboxes from a list of file paths."""

        self.targets = targets
        self.target_vars.clear()

        for widget in self.target_frame_scroll.winfo_children():
            widget.destroy()

        for file_path in sorted(self.targets):
            var = tk.BooleanVar(value=False)
            self.target_vars[file_path] = var

            name = file_path.split("/")[-1]

            ttk.Checkbutton(
                self.target_frame_scroll,
                text=name,
                variable=var,
            ).pack(anchor="w", fill="x", padx=5, pady=2)

        self.update_count()

    def select_all_targets(self):
        for var in self.target_vars.values():
            var.set(True)
        self.update_count()

    def deselect_all_targets(self):
        for var in self.target_vars.values():
            var.set(False)
        self.update_count()

    def get_selected_targets(self):
        return [fp for fp, var in self.target_vars.items() if var.get()]

    def update_count(self):
        selected = sum(var.get() for var in self.target_vars.values())
        total = len(self.target_vars)
        self.targets_label.config(text=f"Targets ({selected}/{total})")
