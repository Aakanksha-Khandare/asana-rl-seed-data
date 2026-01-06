"""
Project data generator.
"""

import random
from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date
from src.config import (
    NUM_PROJECTS,
    PROJECT_TYPE_BY_TEAM,
    PROJECT_TYPES
)


PROJECT_NAME_TEMPLATES = {
    "sprint": [
        "Sprint {n} - Core Platform",
        "Sprint {n} - Feature Delivery",
        "Sprint {n} - Stability Improvements"
    ],
    "kanban": [
        "Bug Tracking Board",
        "Technical Debt Backlog",
        "Operational Requests"
    ],
    "campaign": [
        "Q{n} Product Launch",
        "Brand Awareness Campaign",
        "Lead Generation Campaign"
    ],
    "ongoing": [
        "Product Roadmap",
        "Customer Requests",
        "Internal Improvements"
    ]
}


def generate_projects(workspace_id, teams, users):
    """
    Generate projects owned by teams.
    """

    projects = []
    user_ids = [u["user_id"] for u in users]

    for team in teams:
        team_type = team["team_type"]
        possible_types = PROJECT_TYPE_BY_TEAM.get(team_type, ["ongoing"])

        num_projects = random.randint(5, 10)

        for i in range(num_projects):
            project_type = random.choice(possible_types)
            name_template = random.choice(PROJECT_NAME_TEMPLATES[project_type])

            project_name = name_template.format(n=random.randint(1, 4))

            projects.append({
                "project_id": generate_uuid(),
                "workspace_id": workspace_id,
                "team_id": team["team_id"],
                "name": project_name,
                "description": f"{project_name} project",
                "project_type": project_type,
                "status": "active",
                "privacy": "team",
                "owner_id": random.choice(user_ids),
                "created_at": generate_creation_date(),
                "color": "light-gray"
            })

    return projects
