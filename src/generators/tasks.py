"""
Task and subtask data generator.
"""

import random
from src.utils.string_utils import generate_uuid, truncate_string
from src.utils.date_utils import (
    generate_creation_date,
    generate_due_date,
    generate_completion_date
)
from src.config import (
    TASKS_PER_PROJECT_MIN,
    TASKS_PER_PROJECT_MAX,
    SUBTASK_PROBABILITY,
    SUBTASKS_PER_TASK_MIN,
    SUBTASKS_PER_TASK_MAX,
    PRIORITY_DISTRIBUTION,
    COMPLETION_RATES
)


TASK_NAME_TEMPLATES = {
    "engineering": [
        "Implement {feature} for {component}",
        "Fix {issue} in {component}",
        "Refactor {component} - {reason}",
        "{component} - Improve performance"
    ],
    "marketing": [
        "Create {asset} for {campaign}",
        "{campaign} - Publish content",
        "Design {asset} for {channel}",
        "{campaign} - Launch execution"
    ],
    "product": [
        "Define requirements for {feature}",
        "User testing - {feature}",
        "Roadmap planning for {feature}",
        "Analyze feedback for {feature}"
    ],
    "operations": [
        "Optimize {process}",
        "Document {process}",
        "Setup {tool} for team",
        "{process} - Process improvement"
    ],
    "sales": [
        "Follow up with {prospect}",
        "Prepare proposal for {prospect}",
        "Pipeline review - {stage}",
        "Customer outreach"
    ]
}


def weighted_choice(weight_dict):
    r = random.random()
    cumulative = 0.0
    for key, weight in weight_dict.items():
        cumulative += weight
        if r <= cumulative:
            return key
    return None


def generate_tasks(projects, sections, teams, users):
    """
    Generate tasks and subtasks for projects.
    """
    tasks = []

    # Quick lookup maps
    sections_by_project = {}
    for s in sections:
        sections_by_project.setdefault(s["project_id"], []).append(s)

    users_by_team = {}
    for u in users:
        users_by_team.setdefault(u["workspace_id"], []).append(u["user_id"])

    for project in projects:
        project_id = project["project_id"]
        project_type = project["project_type"]

        project_sections = sorted(
            sections_by_project[project_id],
            key=lambda x: x["display_order"]
        )

        num_tasks = random.randint(TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX)
        completion_low, completion_high = COMPLETION_RATES[project_type]
        completion_rate = random.uniform(completion_low, completion_high)

        for _ in range(num_tasks):
            created_at = generate_creation_date()
            due_date = generate_due_date(created_at, project_type)

            completed = random.random() < completion_rate
            completed_at = (
                generate_completion_date(created_at, due_date)
                if completed else None
            )

            priority = weighted_choice(PRIORITY_DISTRIBUTION)

            section = random.choice(project_sections)

            task_id = generate_uuid()
            task = {
                "task_id": task_id,
                "project_id": project_id,
                "section_id": section["section_id"],
                "parent_task_id": None,
                "name": truncate_string(
                    f"{project_type.capitalize()} Task - {random.randint(1, 999)}",
                    200
                ),
                "description": None,
                "assignee_id": random.choice(users)[
                    "user_id"
                ] if random.random() > 0.15 else None,
                "created_by": random.choice(users)["user_id"],
                "created_at": created_at,
                "modified_at": completed_at or created_at,
                "start_date": None,
                "due_date": due_date,
                "completed": int(completed),
                "completed_at": completed_at,
                "priority": priority,
                "estimated_hours": round(random.uniform(1, 16), 1),
                "actual_hours": round(random.uniform(1, 20), 1) if completed else None
            }

            tasks.append(task)

            # ---------------- SUBTASKS ----------------
            if random.random() < SUBTASK_PROBABILITY:
                num_subtasks = random.randint(
                    SUBTASKS_PER_TASK_MIN,
                    SUBTASKS_PER_TASK_MAX
                )

                for i in range(num_subtasks):
                    subtask_id = generate_uuid()
                    subtask = {
                        "task_id": subtask_id,
                        "project_id": project_id,
                        "section_id": section["section_id"],
                        "parent_task_id": task_id,
                        "name": truncate_string(
                            f"Subtask {i + 1} for task",
                            200
                        ),
                        "description": None,
                        "assignee_id": task["assignee_id"],
                        "created_by": task["created_by"],
                        "created_at": created_at,
                        "modified_at": completed_at or created_at,
                        "start_date": None,
                        "due_date": due_date,
                        "completed": int(completed),
                        "completed_at": completed_at,
                        "priority": priority,
                        "estimated_hours": round(random.uniform(0.5, 8), 1),
                        "actual_hours": round(random.uniform(0.5, 10), 1) if completed else None
                    }

                    tasks.append(subtask)

    return tasks
