"""
Section 1: Intelligent Email and Password Validator using Regular Expressions
Validates Email, Password and Mobile Number according to the given policies.
"""
import re
import sys

# ---------------------------------------------------------------- patterns
# Email: starts with an alphabet, letters/digits/'.'/'_' before '@',
# domain contains only alphabets, extension in (com, org, edu, net, in)
EMAIL_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._]*@[A-Za-z]+\.(com|org|edu|net|in)$")

# Password: min 8 chars, upper, lower, digit and special character (@#$%&!)
PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&!]).{8,}$")

# Mobile: exactly 10 digits, first digit between 6 and 9
MOBILE_PATTERN = re.compile(r"^[6-9]\d{9}$")


# --------------------------------------------------------------- validators
def validate_email(email: str) -> str:
    return "Valid Email" if EMAIL_PATTERN.match(email) else "Invalid Email"


def validate_password(password: str) -> str:
    return "Strong Password" if PASSWORD_PATTERN.match(password) else "Weak Password"


def validate_mobile(mobile: str) -> str:
    return "Valid Mobile Number" if MOBILE_PATTERN.match(mobile) else "Invalid Mobile Number"


def run_test_cases() -> None:
    """Display input, processing (pattern used) and output for test cases."""
    tests = [
        ("Email", validate_email, [
            "john.doe@gmail.com", "alice_99@university.edu", "student@saveetha.in",
            "1john@gmail.com", "john@gmail123.com", "john@gmail.xyz", "john@@gmail.com"]),
        ("Password", validate_password, [
            "Secure@123", "Pass#word9", "password", "PASSWORD@1", "Pass@12", "NoSpecial123"]),
        ("Mobile", validate_mobile, [
            "9876543210", "6123456789", "5876543210", "98765432", "98765432101", "98765abcde"]),
    ]
    for name, func, cases in tests:
        print(f"--- {name} Validation Test Cases ---")
        for value in cases:
            print(f"Input: {value:<26} -> {func(value)}")
        print()


def read_input(prompt: str) -> str:
    """Read a line; echo it when input is piped so the run is self-explanatory."""
    try:
        value = input(prompt)
    except EOFError:
        value = ""
    if not sys.stdin.isatty():
        print(value)
    return value.strip()


def main() -> None:
    print("=" * 56)
    print(" USER REGISTRATION - CREDENTIAL VALIDATOR")
    print("=" * 56)
    print()
    run_test_cases()
    print("--- Enter your own credentials ---")
    email = read_input("Enter Email           : ")
    password = read_input("Enter Password        : ")
    mobile = read_input("Enter Mobile Number   : ")
    print()
    print("Result")
    print("Email    :", validate_email(email))
    print("Password :", validate_password(password))
    print("Mobile   :", validate_mobile(mobile))


if __name__ == "__main__":
    main()
