import re

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


def validate_field(field, value):
    pattern, requirement = RULES[field]
    if not isinstance(value, str) or not value.strip():
        return False, f"{field}: Invalid - field is empty"
    if pattern.fullmatch(value.strip()):
        return True, f"{field}: Valid"
    return False, f"{field}: Invalid - {requirement}"


def validate_student(record):
    results = []
    for field in RULES:
        results.append(validate_field(field, record.get(field, "")))
    return results


def registration_report(record):
    results = validate_student(record)
    print(f"Student record : {record.get('Register Number', '') or '(blank)'}")
    print("-" * 66)
    for _, message in results:
        print(message)
    failed = sum(1 for passed, _ in results if not passed)
    print("-" * 66)
    if failed == 0:
        print("REGISTRATION STATUS: SUCCESSFUL")
    else:
        print(f"REGISTRATION STATUS: FAILED ({failed} field(s) invalid)")
    print()
    return failed == 0


def main():
    records = [
        {
            "Register Number": "192311025",
            "Institutional Email": "arun.kumar@simats.edu.in",
            "Course Code": "DSA03",
            "Semester": "5",
            "Mobile Number": "+91 9876543210",
        },
        {
            "Register Number": "19231102",
            "Institutional Email": "priya.s@gmail.com",
            "Course Code": "dsa03",
            "Semester": "9",
            "Mobile Number": "5123456789",
        },
        {
            "Register Number": "212411067",
            "Institutional Email": "rahul_m@simats.edu.in",
            "Course Code": "CSA12",
            "Semester": "Semester 3",
            "Mobile Number": "98765432",
        },
        {
            "Register Number": "202211340",
            "Institutional Email": "divya.l@simats.edu.in",
            "Course Code": "ITA101",
            "Semester": "8",
            "Mobile Number": "7012345678",
        },
        {
            "Register Number": "",
            "Institutional Email": "",
            "Course Code": "",
            "Semester": "",
            "Mobile Number": "",
        },
    ]

    print("=" * 66)
    print("UNIVERSITY REGISTRATION VALIDATION SYSTEM")
    print("=" * 66)
    print()

    outcomes = [registration_report(record) for record in records]

    print("=" * 66)
    print("FINAL SUMMARY")
    print("=" * 66)
    print(f"Total applications : {len(outcomes)}")
    print(f"Successful         : {sum(outcomes)}")
    print(f"Failed             : {len(outcomes) - sum(outcomes)}")


if __name__ == "__main__":
    main()
