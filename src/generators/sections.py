"""
Section data generator.
"""

from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date
from src.config import PROJECT_TYPES


def generate_sections(projects):
    """
    Generate workflow sections for each project.
    """

    sections = []

    for project in projects:
        project_type = project["project_type"]
        section_names = PROJECT_TYPES[project_type]["sections"]

        for order, name in enumerate(section_names):
            sections.append({
                "section_id": generate_uuid(),
                "project_id": project["project_id"],
                "name": name,
                "display_order": order,
                "created_at": generate_creation_date()
            })

    return sections
