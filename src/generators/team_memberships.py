"""
Team membership data generator.
"""

import random
from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date
from src.config import USERS_PER_TEAM_MIN, USERS_PER_TEAM_MAX


def generate_team_memberships(users, teams):
    """
    Assign users to teams.

    Ensures:
    - No duplicate (team_id, user_id) pairs
    - Each team has realistic membership size
    """

    memberships = []
    used_pairs = set()

    user_ids = [u["user_id"] for u in users]

    for team in teams:
        team_id = team["team_id"]

        num_members = random.randint(USERS_PER_TEAM_MIN, USERS_PER_TEAM_MAX)
        selected_users = random.sample(user_ids, min(num_members, len(user_ids)))

        for user_id in selected_users:
            pair = (team_id, user_id)

            if pair in used_pairs:
                continue  # skip duplicate

            used_pairs.add(pair)

            memberships.append({
                "membership_id": generate_uuid(),
                "team_id": team_id,
                "user_id": user_id,
                "joined_at": generate_creation_date()
            })

    return memberships
