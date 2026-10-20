import re

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


def run_search(products, keyword, mode, ignore_case=True):
    try:
        matches = search_products(products, keyword, mode, ignore_case)
    except ValueError as error:
        print(f"Error: {error}\n")
        return None
    case_label = "Case-insensitive" if ignore_case else "Case-sensitive"
    print(f"Search type : {mode.capitalize()} ({case_label})")
    print(f"Keyword     : '{keyword}'")
    if matches:
        for position, name in enumerate(matches, start=1):
            print(f"  {position}. {name}")
    else:
        print("  No matching products found.")
    print(f"Matches     : {len(matches)}\n")
    return len(matches)


def print_report(results):
    print("=" * 62)
    print("SEARCH SUMMARY REPORT")
    print("=" * 62)
    print(f"{'No.':<5}{'Search Type':<22}{'Keyword':<16}{'Matches':>8}")
    print("-" * 62)
    for number, (label, keyword, count) in enumerate(results, start=1):
        print(f"{number:<5}{label:<22}{keyword:<16}{count:>8}")
    print("-" * 62)
    print(f"{'Total searches performed':<43}{len(results):>19}")
    print(f"{'Total matches across searches':<43}{sum(r[2] for r in results):>19}")


def main():
    searches = [
        ("Exact", "laptop", "exact", True),
        ("Prefix", "head", "prefix", True),
        ("Suffix", "phone", "suffix", True),
        ("Partial", "board", "partial", True),
        ("Case-insensitive", "WIRELESS", "exact", True),
        ("Case-sensitive", "WIRELESS", "exact", False),
        ("Exact", "tablet", "exact", True),
    ]

    print("=" * 62)
    print("PRODUCT SEARCH SYSTEM")
    print("=" * 62)
    print(f"Catalogue size: {len(PRODUCTS)} products\n")

    results = []
    for label, keyword, mode, ignore_case in searches:
        count = run_search(PRODUCTS, keyword, mode, ignore_case)
        results.append((label, keyword, count))

    run_search(PRODUCTS, "   ", "exact")

    print_report(results)


if __name__ == "__main__":
    main()
