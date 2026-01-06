"""
Custom field definitions and values generator.
"""

import random
import json
from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date
from src.config import PROJECT_TYPES


def generate_custom_field_definitions(projects):
    """
    Generate custom field definitions per project.
    """

    field_defs = []

    for project in projects:
        project_type = project["project_type"]
        fields = PROJECT_TYPES[project_type]["custom_fields"]

        for field in fields:
            field_defs.append({
                "field_id": generate_uuid(),
                "project_id": project["project_id"],
                "field_name": field["name"],
                "field_type": field["type"],
                "enum_options": json.dumps(field.get("options")) if "options" in field else None,
                "is_required": 0,
                "created_at": generate_creation_date()
            })

    return field_defs


def generate_custom_field_values(tasks, field_defs):
    """
    Assign values to custom fields at the task level.
    """

    values = []

    fields_by_project = {}
    for f in field_defs:
        fields_by_project.setdefault(f["project_id"], []).append(f)

    for task in tasks:
        project_fields = fields_by_project.get(task["project_id"], [])

        for field in project_fields:
            field_type = field["field_type"]

            if field_type == "number":
                value = str(random.randint(1, 13))
            elif field_type == "enum":
                options = json.loads(field["enum_options"])
                value = random.choice(options)
            else:
                continue

            values.append({
                "value_id": generate_uuid(),
                "field_id": field["field_id"],
                "task_id": task["task_id"],
                "value": value
            })

    return values
