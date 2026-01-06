"""
String generation utilities for creating realistic text content.
"""

import random
import uuid


def generate_uuid():
    """
    Generate a UUID (Universally Unique Identifier).
    
    Asana uses GIDs (Global IDs) which are similar to UUIDs.
    
    Returns:
        str: A UUID string
    """
    return str(uuid.uuid4())


def generate_email(first_name, last_name, domain):
    """
    Generate a realistic email address.
    
    Args:
        first_name: Person's first name
        last_name: Person's last name
        domain: Company domain
    
    Returns:
        str: Email address
    """
    # Convert to lowercase, remove spaces
    first = first_name.lower().replace(' ', '')
    last = last_name.lower().replace(' ', '')
    
    # Common email patterns
    patterns = [
        f"{first}.{last}@{domain}",           # john.doe@company.com
        f"{first}{last}@{domain}",            # johndoe@company.com
        f"{first[0]}{last}@{domain}",         # jdoe@company.com
        f"{first}_{last}@{domain}",           # john_doe@company.com
    ]
    
    return random.choice(patterns)


def truncate_string(text, max_length):
    """
    Truncate a string to max length, adding ellipsis if needed.
    
    Args:
        text: String to truncate
        max_length: Maximum length
    
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def clean_string(text):
    """
    Clean a string for database insertion.
    
    Removes extra whitespace, newlines, etc.
    
    Args:
        text: String to clean
    
    Returns:
        str: Cleaned string
    """
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


def capitalize_title(text):
    """
    Capitalize a title properly.
    
    Example: "fix login button" → "Fix Login Button"
    
    Args:
        text: String to capitalize
    
    Returns:
        str: Title-cased string
    """
    # Don't capitalize small words unless they're first
    small_words = ['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'from', 'by', 'in', 'of']
    
    words = text.split()
    capitalized = []
    
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in small_words:
            capitalized.append(word.capitalize())
        else:
            capitalized.append(word.lower())
    
    return ' '.join(capitalized)