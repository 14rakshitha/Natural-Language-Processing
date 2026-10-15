import re
import tkinter as tk
from tkinter import ttk, messagebox

NAME_PATTERN = re.compile(r"^\s*Name\s*[:\-]\s*([A-Za-z][A-Za-z .']+?)\s*$", re.MULTILINE)
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
MOBILE_PATTERN = re.compile(r"(?<!\d)(?:\+91[\s-]?|0)?([6-9]\d{4}[\s-]?\d{5})(?!\d)")
EXPERIENCE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b", re.IGNORECASE)
SPLIT_PATTERN = re.compile(r"\n\s*-{3,}\s*\n")
SKILL_LIST = ["Python", "Java", "SQL", "Machine Learning", "NLP"]
SKILL_PATTERNS = {
    skill: re.compile(r"(?<![A-Za-z])" + re.escape(skill).replace(r"\ ", r"\s+") + r"(?![A-Za-z])", re.IGNORECASE)
    for skill in SKILL_LIST
}

SAMPLE_RESUMES = """Name: Arun Kumar
Email: arun.kumar@gmail.com
Mobile: +91 98765 43210
Skills: Python, SQL, Machine Learning
Experience: 3 years as a data analyst
---
Name: Priya Sharma
Email: priya_sharma92@outlook.com
Phone: 9123456780
Skills: Java, SQL
Experience: 4.5 years in backend development
---
Name: Rahul Menon
Email: rahul.menon@company.co.in
Contact: 8012345678
Skills: python, NLP, machine learning
Experience: 1 year of internship experience
---
Name: Divya Lakshmi
Email: divya.lakshmi@yahoo.com
Mobile: +91-70123-45678
Skills: Python, Java, NLP
Experience: 2 years in text analytics
---
Name: Karthik Raja
Email: karthik.raja@@mail
Mobile: 12345
Skills: Excel, Tableau
Experience: 6 years in reporting"""


def extract_name(text):
    match = NAME_PATTERN.search(text)
    return match.group(1).strip() if match else "Not found"


def extract_emails(text):
    return EMAIL_PATTERN.findall(text)


def extract_mobiles(text):
    return [re.sub(r"[\s-]", "", number) for number in MOBILE_PATTERN.findall(text)]


def extract_skills(text):
    return [skill for skill, pattern in SKILL_PATTERNS.items() if pattern.search(text)]


def extract_experience(text):
    values = [float(value) for value in EXPERIENCE_PATTERN.findall(text)]
    return max(values) if values else 0.0


def build_profile(text):
    return {
        "name": extract_name(text),
        "emails": extract_emails(text),
        "mobiles": extract_mobiles(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
    }


def is_eligible(profile, min_experience=2.0, required_skill="Python"):
    return profile["experience"] >= min_experience and required_skill in profile["skills"]


class ResumeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resume Information Extraction System")
        self.geometry("1420x760")
        self.minsize(1300, 680)
        self.configure(bg="#eef2f7")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabelframe", background="#eef2f7")
        self.style.configure("TLabelframe.Label", background="#eef2f7", foreground="#1f3a5f", font=("Segoe UI", 10, "bold"))
        self.style.configure("TRadiobutton", background="#eef2f7")
        self.style.configure("TCheckbutton", background="#eef2f7")
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#1f3a5f", foreground="white")
        self.style.map("Treeview.Heading", background=[("active", "#2c5282")])
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        self.build_header()
        self.build_body()
        self.build_status()

    def build_header(self):
        header = tk.Frame(self, bg="#1f3a5f")
        header.pack(fill="x")
        tk.Label(header, text="Resume Information Extraction System", bg="#1f3a5f", fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(14, 0))
        tk.Label(header, text="DSA03 Natural Language Processing  |  Regex-Based Information Extraction",
                 bg="#1f3a5f", fg="#c8d6ea", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(0, 14))

    def build_body(self):
        body = tk.Frame(self, bg="#eef2f7")
        body.pack(fill="both", expand=True, padx=16, pady=12)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = ttk.LabelFrame(body, text=" Resume Text (separate resumes with a line of ---) ")
        left.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        self.input_box = tk.Text(left, width=38, height=24, font=("Consolas", 10), wrap="word", relief="flat",
                                 bg="white", padx=8, pady=8)
        scroll = ttk.Scrollbar(left, command=self.input_box.yview)
        self.input_box.configure(yscrollcommand=scroll.set)
        self.input_box.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        scroll.grid(row=0, column=1, sticky="ns", pady=8, padx=(0, 8))
        buttons = tk.Frame(left, bg=self.cget("bg"))
        buttons.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        ttk.Button(buttons, text="Load Sample Resumes", style="Action.TButton", command=self.load_sample).grid(row=0, column=0, padx=4)
        ttk.Button(buttons, text="Extract", style="Action.TButton", command=self.extract).grid(row=0, column=1, padx=4)
        ttk.Button(buttons, text="Clear", style="Action.TButton", command=self.clear).grid(row=0, column=2, padx=4)

        right = tk.Frame(body, bg="#eef2f7")
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=3)
        right.rowconfigure(1, weight=2)
        right.columnconfigure(0, weight=1)

        table_frame = ttk.LabelFrame(right, text=" Candidate Profiles ")
        table_frame.grid(row=0, column=0, sticky="nsew")
        columns = ("name", "email", "mobile", "skills", "exp", "status")
        headings = ("Name", "Email", "Mobile", "Skills", "Experience", "Eligibility")
        widths = (105, 215, 95, 260, 85, 90)
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        for column, heading, width in zip(columns, headings, widths):
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, anchor="w")
        self.table.tag_configure("eligible", background="#dff5e1")
        self.table.tag_configure("rejected", background="#fbe3e3")
        self.table.pack(fill="both", expand=True, padx=8, pady=8)

        short_frame = ttk.LabelFrame(right, text=" Shortlisted Candidates (minimum 2 years and Python) ")
        short_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        self.short_box = tk.Text(short_frame, height=8, font=("Consolas", 10), relief="flat", bg="white", padx=10, pady=8, state="disabled")
        self.short_box.pack(fill="both", expand=True, padx=8, pady=8)

    def build_status(self):
        self.status = tk.StringVar(value="Ready. Paste resumes or load the sample data.")
        tk.Label(self, textvariable=self.status, anchor="w", bg="#d9e2ef", fg="#1f3a5f",
                 font=("Segoe UI", 10), padx=14, pady=6).pack(fill="x", side="bottom")

    def load_sample(self):
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", SAMPLE_RESUMES)
        self.status.set("Sample resumes loaded. Click Extract to process them.")

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.table.delete(*self.table.get_children())
        self.write_shortlist("")
        self.status.set("Cleared.")

    def write_shortlist(self, text):
        self.short_box.configure(state="normal")
        self.short_box.delete("1.0", "end")
        self.short_box.insert("1.0", text)
        self.short_box.configure(state="disabled")

    def extract(self):
        raw = self.input_box.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("No input", "Please enter or load at least one resume.")
            return
        resumes = [part for part in SPLIT_PATTERN.split(raw) if part.strip()]
        profiles = [build_profile(resume) for resume in resumes]
        self.table.delete(*self.table.get_children())
        shortlist = []
        for profile in profiles:
            eligible = is_eligible(profile)
            unit = "year" if profile["experience"] == 1 else "years"
            self.table.insert("", "end", tags=("eligible" if eligible else "rejected",), values=(
                profile["name"],
                ", ".join(profile["emails"]) or "Not found",
                ", ".join(profile["mobiles"]) or "Not found",
                ", ".join(profile["skills"]) or "None detected",
                f"{profile['experience']:g} {unit}",
                "Eligible" if eligible else "Not eligible",
            ))
            if eligible:
                shortlist.append(profile)
        if shortlist:
            lines = [f"{p['name']:<16} {p['experience']:g} yrs   {', '.join(p['skills'])}" for p in shortlist]
            self.write_shortlist("\n".join(lines))
        else:
            self.write_shortlist("No candidate satisfies the criteria.")
        self.status.set(f"Processed {len(profiles)} resumes  |  Shortlisted {len(shortlist)}")


if __name__ == "__main__":
    ResumeApp().mainloop()
