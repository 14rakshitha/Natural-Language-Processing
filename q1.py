import re

NAME_PATTERN = re.compile(r"^\s*Name\s*[:\-]\s*([A-Za-z][A-Za-z .']+?)\s*$", re.MULTILINE)
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
MOBILE_PATTERN = re.compile(r"(?<!\d)(?:\+91[\s-]?|0)?([6-9]\d{4}[\s-]?\d{5})(?!\d)")
EXPERIENCE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b", re.IGNORECASE)
SKILL_LIST = ["Python", "Java", "SQL", "Machine Learning", "NLP"]
SKILL_PATTERNS = {
    skill: re.compile(r"(?<![A-Za-z])" + re.escape(skill).replace(r"\ ", r"\s+") + r"(?![A-Za-z])", re.IGNORECASE)
    for skill in SKILL_LIST
}


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


def print_profile(index, profile):
    print(f"Candidate {index}")
    print("-" * 52)
    print(f"Name        : {profile['name']}")
    print(f"Email       : {', '.join(profile['emails']) or 'Not found'}")
    print(f"Mobile      : {', '.join(profile['mobiles']) or 'Not found'}")
    print(f"Skills      : {', '.join(profile['skills']) or 'None detected'}")
    unit = "year" if profile["experience"] == 1 else "years"
    print(f"Experience  : {profile['experience']:g} {unit}")
    print(f"Eligibility : {'Eligible' if is_eligible(profile) else 'Not eligible'}")
    print()


def main():
    resumes = [
        """Name: Arun Kumar
Email: arun.kumar@gmail.com
Mobile: +91 98765 43210
Skills: Python, SQL, Machine Learning
Experience: 3 years as a data analyst""",
        """Name: Priya Sharma
Email: priya_sharma92@outlook.com
Phone: 9123456780
Skills: Java, SQL
Experience: 4.5 years in backend development""",
        """Name: Rahul Menon
Email: rahul.menon@company.co.in
Contact: 8012345678
Skills: python, NLP, machine learning
Experience: 1 year of internship experience""",
        """Name: Divya Lakshmi
Email: divya.lakshmi@yahoo.com
Mobile: +91-70123-45678
Skills: Python, Java, NLP
Experience: 2 years in text analytics""",
        """Name: Karthik Raja
Email: karthik.raja@@mail
Mobile: 12345
Skills: Excel, Tableau
Experience: 6 years in reporting""",
    ]

    profiles = [build_profile(resume) for resume in resumes]

    print("=" * 52)
    print("RESUME INFORMATION EXTRACTION REPORT")
    print("=" * 52)
    for index, profile in enumerate(profiles, start=1):
        print_profile(index, profile)

    shortlisted = [profile for profile in profiles if is_eligible(profile)]
    print("=" * 52)
    print("SHORTLISTED CANDIDATES (>= 2 years and Python)")
    print("=" * 52)
    if shortlisted:
        for profile in shortlisted:
            print(f"{profile['name']:<16} | {profile['experience']:g} yrs | {', '.join(profile['skills'])}")
    else:
        print("No candidate satisfies the criteria.")
    print(f"\nTotal resumes processed : {len(profiles)}")
    print(f"Total shortlisted       : {len(shortlisted)}")


if __name__ == "__main__":
    main()
