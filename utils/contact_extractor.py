import re

TARGET_TITLES = {
    "ceo": ["ceo", "chief executive", "president", "general manager", "gm"],
    "procurement": ["procurement", "purchasing", "buyer", "sourcing"],
    "mow": ["maintenance of way", "mow", "roadmaster", "track supervisor"],
    "engineering": ["engineering", "engineer", "chief engineer", "civil engineer"],
}

ADDRESS_PATTERN = r"\d{1,6}\s[\w\s.,]+(?:Street|St|Ave|Avenue|Road|Rd|Boulevard|Blvd|Highway|Hwy|Way|Lane|Ln|Drive|Dr)[\s,]+[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}"

def extract_contacts(text):
    contacts = {k: None for k in TARGET_TITLES}
    lines = text.split("\n")

    for line in lines:
        clean = line.strip()
        name_match = re.search(r"[A-Z][a-z]+\s[A-Z][A-Za-z\-]+", clean)
        if not name_match:
            continue

        name = name_match.group(0)
        l = clean.lower()

        for role, keywords in TARGET_TITLES.items():
            if any(k in l for k in keywords) and contacts[role] is None:
                contacts[role] = {
                    "name": name,
                    "raw_line": clean
                }
    return contacts

def extract_address(text):
    match = re.search(ADDRESS_PATTERN, text)
    return match.group(0) if match else None
