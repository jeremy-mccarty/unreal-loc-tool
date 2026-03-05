from tkinter import ttk

def form_row(parent, row, label_text, entry_widget, button=None):
    label = ttk.Label(parent, text=label_text)

    label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
    entry_widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

    if button:
        button.grid(row=row, column=2, padx=5, pady=5)

    parent.grid_columnconfigure(1, weight=1)