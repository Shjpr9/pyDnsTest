import re
import json
import os

INPUT_FILE = "list.txt"

def extract_ips():
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # Matches IPv4
    pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    return re.findall(pattern, content)

import json
import os

def add_result_to_json(domain, ips, asn, filename="domain_ips.json"):
    """
    Add a single result to the JSON file with support for multiple IPs.
    
    Args:
        domain: Domain name (e.g., "google.com")
        ips: Single IP string OR list of IP strings
        asn: ASN information
        filename: JSON file name
    """
    # Convert single IP to list for consistency
    if isinstance(ips, str):
        ips = [ips]
    
    # Load existing data if file exists
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}
    else:
        data = {}
    
    # Add/update the result
    data[domain] = {
        "ips": ips,  # Now stores an array of IPs
        "asn": asn
    }
    
    # Save back to file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Added/Updated {domain} in {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

