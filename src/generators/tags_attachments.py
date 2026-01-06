"""
Tag and attachment data generator.
"""

import random
from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date
from src.config import COMMON_TAGS, ATTACHMENT_PROBABILITY, TAG_PROBABILITY


def generate_tags(workspace_id):
    """
    Generate workspace-level tags.
    """
    tags = []

    for tag in COMMON_TAGS:
        tags.append({
            "tag_id": generate_uuid(),
            "workspace_id": workspace_id,
            "name": tag["name"],
            "color": tag["color"],
            "created_at": generate_creation_date()
        })

    return tags


def generate_task_tags(tasks, tags):
    """
    Assign tags to a subset of tasks.
    """
    task_tags = []

    for task in tasks:
        if random.random() < TAG_PROBABILITY:
            selected = random.sample(tags, random.randint(1, min(2, len(tags))))

            for tag in selected:
                task_tags.append({
                    "task_tag_id": generate_uuid(),
                    "task_id": task["task_id"],
                    "tag_id": tag["tag_id"],
                    "created_at": generate_creation_date()
                })

    return task_tags


def generate_attachments(tasks, users):
    """
    Generate attachments for a subset of tasks.
    """
    attachments = []

    for task in tasks:
        if random.random() < ATTACHMENT_PROBABILITY:
            attachments.append({
                "attachment_id": generate_uuid(),
                "task_id": task["task_id"],
                "uploaded_by": random.choice(users)["user_id"],
                "file_name": f"attachment_{random.randint(1,999)}.pdf",
                "file_size": random.randint(50_000, 5_000_000),
                "file_type": "pdf",
                "url": f"https://files.example.com/{generate_uuid()}",
                "uploaded_at": generate_creation_date()
            })

    return attachments
