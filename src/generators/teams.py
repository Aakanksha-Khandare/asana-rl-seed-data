"""
Team data generator.
"""

import random
from src.config import NUM_TEAMS, TEAM_TYPES
from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date


TEAM_NAME_TEMPLATES = {
    "engineering": [
        "Backend Platform",
        "Frontend Experience",
        "Infrastructure",
        "Data Engineering",
        "API Services",
        "Quality Engineering"
    ],
    "product": [
        "Product Strategy",
        "User Experience",
        "Growth Product"
    ],
    "marketing": [
        "Growth Marketing",
        "Brand Marketing",
        "Content Marketing"
    ],
    "operations": [
        "Customer Operations",
        "Internal Operations"
    ],
    "sales": [
        "Enterprise Sales",
        "SMB Sales"
    ]
}


def generate_teams(workspace_id):
    teams = []

    for team_type, count in TEAM_TYPES.items():
        names = TEAM_NAME_TEMPLATES.get(team_type, [])
        random.shuffle(names)

        for i in range(count):
            team_name = names[i % len(names)]

            teams.append({
                "team_id": generate_uuid(),
                "workspace_id": workspace_id,
                "name": team_name,
                "description": f"{team_name} team",
                "team_type": team_type,
                "created_at": generate_creation_date(),
                "is_archived": 0
            })

    return teams
