"""
User data generator.
"""

import random
from src.config import (
    NUM_USERS,
    ADMIN_PERCENTAGE,
    GUEST_PERCENTAGE,
    COMPANY_DOMAIN
)
from src.utils.string_utils import generate_uuid, generate_email
from src.utils.date_utils import generate_creation_date


FIRST_NAMES = ["Amit", "Neha", "Rahul", "Priya", "Ankit", "Sneha", "Vikas", "Pooja"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Singh", "Iyer", "Gupta"]


def generate_users(workspace_id):
    users = []
    used_emails = set()

    for i in range(NUM_USERS):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        role_rand = random.random()
        if role_rand < ADMIN_PERCENTAGE:
            role = "admin"
        elif role_rand < ADMIN_PERCENTAGE + GUEST_PERCENTAGE:
            role = "guest"
        else:
            role = "member"

        # Ensure unique email
        base_email = generate_email(first, last, COMPANY_DOMAIN)
        email = base_email
        counter = 1

        while email in used_emails:
            # Append a numeric suffix to ensure uniqueness
            name, domain = base_email.split("@")
            email = f"{name}{counter}@{domain}"
            counter += 1

        used_emails.add(email)

        users.append({
            "user_id": generate_uuid(),
            "workspace_id": workspace_id,
            "name": f"{first} {last}",
            "email": email,
            "role": role,
            "created_at": generate_creation_date(),
            "is_active": 1
        })

    return users
