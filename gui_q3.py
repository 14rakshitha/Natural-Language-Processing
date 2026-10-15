import re
import tkinter as tk
from tkinter import ttk

RULES = {
    "Register Number": (
        re.compile(r"^(?:19|2[0-6])\d{7}$"),
        "9 digits starting with an admission year between 19 and 26",
    ),
    "Institutional Email": (
        re.compile(r"^[A-Za-z][A-Za-z0-9._-]*@simats\.edu\.in$"),
        "must be of the form name@simats.edu.in",
    ),
    "Course Code": (
        re.compile(r"^[A-Z]{3}\d{2}$"),
        "three capital letters followed by two digits, e.g. DSA03",
    ),
    "Semester": (
        re.compile(r"^(?:Semester\s)?[1-8]$"),
        "a number from 1 to 8, optionally prefixed with 'Semester '",
    ),
    "Mobile Number": (
        re.compile(r"^(?:\+91[\s-]?)?[6-9]\d{9}$"),
        "10 digits starting with 6-9, optional +91 prefix",
    ),
}

VALID_SAMPLE = {
    "Register Number": "192311025",
    "Institutional Email": "arun.kumar@simats.edu.in",
    "Course Code": "DSA03",
    "Semester": "5",
    "Mobile Number": "+91 9876543210",
}

INVALID_SAMPLE = {
    "Register Number": "19231102",
    "Institutional Email": "priya.s@gmail.com",
    "Course Code": "dsa03",
    "Semester": "9",
    "Mobile Number": "5123456789",
}


def validate_field(field, value):
    pattern, requirement = RULES[field]
    if not value.strip():
        return False, "Invalid - field is empty"
    if pattern.fullmatch(value.strip()):
        return True, "Valid"
    return False, f"Invalid - {requirement}"


class RegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Registration Validation System")
        self.geometry("1120x700")
        self.minsize(1050, 660)
        self.configure(bg="#eef3ee")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabelframe", background="#eef3ee")
        self.style.configure("TLabelframe.Label", background="#eef3ee", foreground="#1d5c3a", font=("Segoe UI", 10, "bold"))
        self.style.configure("TRadiobutton", background="#eef3ee")
        self.style.configure("TCheckbutton", background="#eef3ee")
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=9)
        self.vars = {field: tk.StringVar() for field in RULES}
        self.result_labels = {}
        self.build_header()
        self.build_form()
        self.build_banner()

    def build_header(self):
        header = tk.Frame(self, bg="#1d5c3a")
        header.pack(fill="x")
        tk.Label(header, text="University Registration Validation System", bg="#1d5c3a", fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(14, 0))
        tk.Label(header, text="DSA03 Natural Language Processing  |  Regex-Based Input Validation",
                 bg="#1d5c3a", fg="#cfe6d8", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(0, 14))

    def build_form(self):
        box = ttk.LabelFrame(self, text=" Student Registration Form ")
        box.pack(fill="x", padx=20, pady=(16, 8))
        grid = tk.Frame(box, bg=self.cget("bg"))
        grid.pack(fill="x", padx=14, pady=12)
        grid.columnconfigure(2, weight=1)
        for row, field in enumerate(RULES):
            tk.Label(grid, text=field, width=19, anchor="w", bg=self.cget("bg"),
                     font=("Segoe UI", 11, "bold")).grid(row=row, column=0, pady=9, sticky="w")
            ttk.Entry(grid, textvariable=self.vars[field], width=30, font=("Segoe UI", 11)).grid(row=row, column=1, padx=(0, 16))
            label = tk.Label(grid, text="", anchor="w", justify="left", wraplength=500, bg=self.cget("bg"), font=("Segoe UI", 10))
            label.grid(row=row, column=2, sticky="w")
            self.result_labels[field] = label
        buttons = tk.Frame(box, bg=self.cget("bg"))
        buttons.pack(pady=(0, 12))
        ttk.Button(buttons, text="Validate Registration", style="Action.TButton", command=self.validate).grid(row=0, column=0, padx=5)
        ttk.Button(buttons, text="Fill Valid Sample", style="Action.TButton", command=lambda: self.fill(VALID_SAMPLE)).grid(row=0, column=1, padx=5)
        ttk.Button(buttons, text="Fill Invalid Sample", style="Action.TButton", command=lambda: self.fill(INVALID_SAMPLE)).grid(row=0, column=2, padx=5)
        ttk.Button(buttons, text="Clear", style="Action.TButton", command=self.clear).grid(row=0, column=3, padx=5)

    def build_banner(self):
        report = ttk.LabelFrame(self, text=" Final Registration Status ")
        report.pack(fill="both", expand=True, padx=20, pady=(8, 16))
        self.banner = tk.Label(report, text="Awaiting validation", font=("Segoe UI", 20, "bold"), bg="#d9dfd9", fg="#44504a", pady=22)
        self.banner.pack(fill="x", padx=12, pady=(12, 8))
        self.detail = tk.Label(report, text="Fill in the form and click Validate Registration.", font=("Segoe UI", 11),
                               bg=self.cget("bg"), anchor="w")
        self.detail.pack(fill="x", padx=14, pady=(0, 12))

    def fill(self, record):
        for field, value in record.items():
            self.vars[field].set(value)
        self.validate()

    def clear(self):
        for field in RULES:
            self.vars[field].set("")
            self.result_labels[field].configure(text="")
        self.banner.configure(text="Awaiting validation", bg="#d9dfd9", fg="#44504a")
        self.detail.configure(text="Fill in the form and click Validate Registration.")

    def validate(self):
        failed = 0
        for field in RULES:
            passed, message = validate_field(field, self.vars[field].get())
            symbol = "\u2714  " if passed else "\u2718  "
            self.result_labels[field].configure(text=symbol + message, fg="#1d7a3f" if passed else "#b3261e")
            failed += 0 if passed else 1
        if failed == 0:
            self.banner.configure(text="REGISTRATION SUCCESSFUL", bg="#cdeed7", fg="#14532d")
            self.detail.configure(text="All five fields passed validation. The student may proceed to course enrollment.")
        else:
            self.banner.configure(text="REGISTRATION FAILED", bg="#f8d4d0", fg="#8a1c14")
            self.detail.configure(text=f"{failed} field(s) failed validation. Correct the highlighted entries and try again.")


if __name__ == "__main__":
    RegistrationApp().mainloop()
