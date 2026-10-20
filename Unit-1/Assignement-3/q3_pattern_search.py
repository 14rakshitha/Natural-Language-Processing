"""
Section 3: Smart Pattern Matching Engine using Regular Expressions
Supports Word, Prefix, Suffix, Date, Phone Number, Hashtag and Mention search.
"""
import re
import sys

SAMPLE_TEXT = """Meeting on 12/09/2026
Call 9876543210
#NLP
@OpenAI
natural language processing"""

DATE_PATTERN = r"\b\d{1,2}/\d{1,2}/\d{4}\b"
PHONE_PATTERN = r"\b[6-9]\d{9}\b"
HASHTAG_PATTERN = r"#\w+"
MENTION_PATTERN = r"@\w+"


def search_pattern(pattern: str, text: str):
    return re.findall(pattern, text, flags=re.IGNORECASE)


def search_word(word: str, text: str):
    return re.findall(rf"\b{re.escape(word)}\b", text, flags=re.IGNORECASE)


def search_prefix(prefix: str, text: str):
    return re.findall(rf"\b{re.escape(prefix)}\w*", text, flags=re.IGNORECASE)


def search_suffix(suffix: str, text: str):
    return re.findall(rf"\b\w*{re.escape(suffix)}\b", text, flags=re.IGNORECASE)


def read_input(prompt: str) -> str:
    try:
        value = input(prompt)
    except EOFError:
        value = "0"
    if not sys.stdin.isatty():
        print(value)
    return value.strip()


def show(title: str, matches) -> None:
    if matches:
        print(f"{title} found ({len(matches)}):")
        for item in matches:
            print("   ", item)
    else:
        print(f"No {title.lower()} found")


def menu() -> None:
    print("\nUser Menu")
    print("1.Search Date")
    print("2.Search Phone Number")
    print("3.Search Hashtag")
    print("4.Search Mention")
    print("5.Search Prefix")
    print("6.Search Suffix")
    print("7.Search Word")
    print("0.Exit")


def main() -> None:
    print("=" * 56)
    print(" SMART PATTERN MATCHING ENGINE")
    print("=" * 56)
    print("Input Text:")
    print(SAMPLE_TEXT)
    text = SAMPLE_TEXT
    while True:
        menu()
        choice = read_input("Enter your choice: ")
        if choice == "1":
            show("Date", search_pattern(DATE_PATTERN, text))
        elif choice == "2":
            show("Phone Number", search_pattern(PHONE_PATTERN, text))
        elif choice == "3":
            show("Hashtag", search_pattern(HASHTAG_PATTERN, text))
        elif choice == "4":
            show("Mention", search_pattern(MENTION_PATTERN, text))
        elif choice == "5":
            prefix = read_input("Enter prefix: ")
            show("Prefix match", search_prefix(prefix, text)) if prefix else print("Prefix cannot be empty")
        elif choice == "6":
            suffix = read_input("Enter suffix: ")
            show("Suffix match", search_suffix(suffix, text)) if suffix else print("Suffix cannot be empty")
        elif choice == "7":
            word = read_input("Enter word: ")
            show("Word match", search_word(word, text)) if word else print("Word cannot be empty")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select 0-7")


if __name__ == "__main__":
    main()
