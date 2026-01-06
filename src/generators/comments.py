"""
Comment (story) data generator.
"""

import random
from src.utils.string_utils import generate_uuid
from src.utils.date_utils import generate_creation_date


COMMENT_TEMPLATES = [
    "Moving this to In Progress.",
    "Any updates on this?",
    "Blocking issue identified, investigating.",
    "Looks good to me.",
    "Please review when you get a chance.",
    "This is now complete.",
    "Adding more context here.",
    "Assigning this to the appropriate owner."
]


def generate_comments(tasks, users):
    """
    Generate comments for a subset of tasks.
    """

    comments = []

    for task in tasks:
        # Not every task has comments
        if random.random() < 0.6:
            num_comments = random.randint(1, 5)

            for _ in range(num_comments):
                comments.append({
                    "comment_id": generate_uuid(),
                    "task_id": task["task_id"],
                    "user_id": random.choice(users)["user_id"],
                    "comment_text": random.choice(COMMENT_TEMPLATES),
                    "created_at": generate_creation_date(),
                    "edited_at": None,
                    "is_edited": 0
                })

    return comments
