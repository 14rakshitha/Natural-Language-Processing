import re
import tkinter as tk
from tkinter import ttk, messagebox

PRODUCTS = [
    "Apple iPhone 15",
    "Samsung Galaxy Phone",
    "Wireless Bluetooth Headphones",
    "Noise Cancelling Headphone",
    "Smart LED Television",
    "Phone Case Silicone",
    "Laptop Backpack",
    "Gaming Laptop",
    "Laptop Stand Adjustable",
    "Mechanical Keyboard",
    "Wireless Keyboard and Mouse",
    "Smartwatch Series 8",
    "Portable Power Bank",
    "USB Phone Charger",
    "Headphone Stand",
]


def build_pattern(keyword, mode):
    if not keyword or not keyword.strip():
        raise ValueError("Search keyword cannot be empty.")
    word = re.escape(keyword.strip())
    patterns = {
        "exact": rf"\b{word}\b",
        "prefix": rf"\b{word}\w*",
        "suffix": rf"\w*{word}\b",
        "partial": rf"{word}",
    }
    if mode not in patterns:
        raise ValueError(f"Unknown search mode: {mode}")
    return patterns[mode]


def search_products(products, keyword, mode, ignore_case=True):
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(build_pattern(keyword, mode), flags)
    return [product for product in products if regex.search(product)]


class SearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product Search System")
        self.geometry("1120x740")
        self.minsize(980, 660)
        self.configure(bg="#f3f1ee")
        self.history = []
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabelframe", background="#f3f1ee")
        self.style.configure("TLabelframe.Label", background="#f3f1ee", foreground="#7a2e1d", font=("Segoe UI", 10, "bold"))
        self.style.configure("TRadiobutton", background="#f3f1ee")
        self.style.configure("TCheckbutton", background="#f3f1ee")
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#7a2e1d", foreground="white")
        self.style.map("Treeview.Heading", background=[("active", "#9c3d28")])
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        self.mode = tk.StringVar(value="exact")
        self.ignore_case = tk.BooleanVar(value=True)
        self.keyword = tk.StringVar()
        self.build_header()
        self.build_controls()
        self.build_results()
        self.build_status()

    def build_header(self):
        header = tk.Frame(self, bg="#7a2e1d")
        header.pack(fill="x")
        tk.Label(header, text="Product Search System", bg="#7a2e1d", fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(14, 0))
        tk.Label(header, text="DSA03 Natural Language Processing  |  Regex Pattern Matching",
                 bg="#7a2e1d", fg="#f0d4cb", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(0, 14))

    def build_controls(self):
        box = ttk.LabelFrame(self, text=" Search ")
        box.pack(fill="x", padx=16, pady=(14, 8))
        row = tk.Frame(box, bg=self.cget("bg"))
        row.pack(fill="x", padx=10, pady=10)
        tk.Label(row, text="Keyword", bg=self.cget("bg"), font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0, 8))
        entry = ttk.Entry(row, textvariable=self.keyword, width=24, font=("Segoe UI", 11))
        entry.grid(row=0, column=1, padx=(0, 18))
        entry.bind("<Return>", lambda event: self.search())
        for column, (label, value) in enumerate([("Exact", "exact"), ("Prefix", "prefix"), ("Suffix", "suffix"), ("Partial", "partial")], start=2):
            ttk.Radiobutton(row, text=label, value=value, variable=self.mode).grid(row=0, column=column, padx=6)
        ttk.Checkbutton(row, text="Ignore case", variable=self.ignore_case).grid(row=0, column=6, padx=(14, 14))
        ttk.Button(row, text="Search", style="Action.TButton", command=self.search).grid(row=0, column=7, padx=4)
        ttk.Button(row, text="Clear Report", style="Action.TButton", command=self.clear_report).grid(row=0, column=8, padx=4)

    def build_results(self):
        body = tk.Frame(self, bg=self.cget("bg"))
        body.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)

        catalogue = ttk.LabelFrame(body, text=" Product Catalogue ")
        catalogue.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        self.catalogue_list = tk.Listbox(catalogue, font=("Segoe UI", 11), activestyle="none", relief="flat", bg="white",
                                         selectbackground="#f6d7a7", selectforeground="black", exportselection=False)
        for product in PRODUCTS:
            self.catalogue_list.insert("end", product)
        self.catalogue_list.pack(fill="both", expand=True, padx=8, pady=8)

        matches = ttk.LabelFrame(body, text=" Matching Products ")
        matches.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
        self.match_list = tk.Listbox(matches, font=("Segoe UI", 11), activestyle="none", relief="flat", bg="white", height=7)
        self.match_list.pack(fill="both", expand=True, padx=8, pady=8)

        report = ttk.LabelFrame(body, text=" Search Report ")
        report.grid(row=1, column=1, sticky="nsew")
        columns = ("no", "type", "keyword", "matches")
        self.report = ttk.Treeview(report, columns=columns, show="headings", height=6)
        for column, heading, width, anchor in [("no", "No.", 40, "center"), ("type", "Search Type", 170, "w"),
                                               ("keyword", "Keyword", 120, "w"), ("matches", "Matches", 70, "center")]:
            self.report.heading(column, text=heading)
            self.report.column(column, width=width, anchor=anchor)
        self.report.pack(fill="both", expand=True, padx=8, pady=(8, 4))
        self.total_label = tk.Label(report, text="Total searches: 0    Total matches: 0", anchor="e",
                                    font=("Segoe UI", 10, "bold"), bg=self.cget("bg"))
        self.total_label.pack(fill="x", padx=10, pady=(0, 8))

    def build_status(self):
        self.status = tk.StringVar(value="Enter a keyword and choose a search type.")
        tk.Label(self, textvariable=self.status, anchor="w", bg="#e4ddd6", fg="#5b2316",
                 font=("Segoe UI", 10), padx=14, pady=6).pack(fill="x", side="bottom")

    def search(self):
        keyword = self.keyword.get()
        mode = self.mode.get()
        try:
            found = search_products(PRODUCTS, keyword, mode, self.ignore_case.get())
        except ValueError as error:
            messagebox.showerror("Invalid search", str(error))
            return
        self.match_list.delete(0, "end")
        self.catalogue_list.selection_clear(0, "end")
        if found:
            for number, name in enumerate(found, start=1):
                self.match_list.insert("end", f"{number}.  {name}")
            for index, product in enumerate(PRODUCTS):
                if product in found:
                    self.catalogue_list.selection_set(index)
        else:
            self.match_list.insert("end", "No matching products found.")
        label = f"{mode.capitalize()} ({'case-insensitive' if self.ignore_case.get() else 'case-sensitive'})"
        self.history.append((label, keyword.strip(), len(found)))
        self.refresh_report()
        self.status.set(f"{label} search for '{keyword.strip()}' returned {len(found)} product(s).")

    def refresh_report(self):
        self.report.delete(*self.report.get_children())
        for number, (label, keyword, count) in enumerate(self.history, start=1):
            self.report.insert("", "end", values=(number, label, keyword, count))
        total = sum(item[2] for item in self.history)
        self.total_label.configure(text=f"Total searches: {len(self.history)}    Total matches: {total}")

    def clear_report(self):
        self.history.clear()
        self.refresh_report()
        self.match_list.delete(0, "end")
        self.catalogue_list.selection_clear(0, "end")
        self.status.set("Report cleared.")


if __name__ == "__main__":
    SearchApp().mainloop()
