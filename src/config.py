"""
Configuration file for Asana seed data generator.
All project parameters and settings are defined here.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_PATH = "output/asana_simulation.sqlite"

# ============================================================================
# COMPANY SCALE CONFIGURATION
# ============================================================================
# Simulating a B2B SaaS company with 5000-10000 employees

# Organization
COMPANY_NAME = "TechFlow Solutions"
COMPANY_DOMAIN = "techflow.com"

# Teams - based on research: typical engineering team size is 7 members
# For a 5000-10000 person company, estimate ~15-20 teams using Asana
NUM_TEAMS = 15
TEAM_TYPES = {
    'engineering': 6,      # 6 engineering teams
    'product': 2,          # 2 product teams
    'marketing': 3,        # 3 marketing teams
    'operations': 2,       # 2 operations teams
    'sales': 2            # 2 sales teams
}

# Users - active Asana users (not entire company)
# Estimate ~150-200 active users for project management
NUM_USERS = 150
USERS_PER_TEAM_MIN = 5
USERS_PER_TEAM_MAX = 12
ADMIN_PERCENTAGE = 0.05  # 5% admins
GUEST_PERCENTAGE = 0.05  # 5% guests

# Projects
NUM_PROJECTS = 120
PROJECTS_PER_TEAM_MIN = 5
PROJECTS_PER_TEAM_MAX = 10

# Tasks
TASKS_PER_PROJECT_MIN = 15
TASKS_PER_PROJECT_MAX = 40
SUBTASK_PROBABILITY = 0.30  # 30% of tasks have subtasks
SUBTASKS_PER_TASK_MIN = 2
SUBTASKS_PER_TASK_MAX = 5

# ============================================================================
# DATE CONFIGURATION
# ============================================================================

# Workspace history - simulating 6 months of activity
WORKSPACE_START_DATE = datetime.now() - timedelta(days=180)  # 6 months ago
CURRENT_DATE = datetime.now()

# Sprint configuration (from research: 2-week sprints are standard)
SPRINT_DURATION_DAYS = 14

# ============================================================================
# TASK DISTRIBUTION PATTERNS
# ============================================================================
# Based on Asana research and industry benchmarks

# Assignment patterns
UNASSIGNED_TASK_PERCENTAGE = 0.15  # 15% tasks unassigned (per Asana data)

# Due date distribution (from research)
# 25% within 1 week, 40% within 1 month, 20% 1-3 months, 10% no due date, 5% overdue
DUE_DATE_DISTRIBUTION = {
    'week_1': 0.25,      # Due within 1 week
    'month_1': 0.40,     # Due within 1 month
    'months_1_3': 0.20,  # Due in 1-3 months
    'no_due_date': 0.10, # No due date
    'overdue': 0.05      # Already overdue
}

# Completion rates by project type (from research)
COMPLETION_RATES = {
    'sprint': (0.70, 0.85),      # 70-85% completion
    'kanban': (0.60, 0.75),      # 60-75% completion
    'campaign': (0.75, 0.85),    # 75-85% completion
    'ongoing': (0.40, 0.50)      # 40-50% completion
}

# Priority distribution
PRIORITY_DISTRIBUTION = {
    'high': 0.15,      # 15% high priority
    'medium': 0.35,    # 35% medium priority
    'low': 0.20,       # 20% low priority
    None: 0.30         # 30% no priority set
}

# ============================================================================
# PROJECT TYPE CONFIGURATIONS
# ============================================================================

PROJECT_TYPES = {
    'sprint': {
        'sections': ['Backlog', 'To Do', 'In Progress', 'In Review', 'Done'],
        'custom_fields': [
            {'name': 'Story Points', 'type': 'number'},
            {'name': 'Sprint', 'type': 'enum', 'options': ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4']},
            {'name': 'Component', 'type': 'enum', 'options': ['Frontend', 'Backend', 'Database', 'API', 'Infrastructure']}
        ],
        'completion_rate': (0.70, 0.85)
    },
    'kanban': {
        'sections': ['Backlog', 'To Do', 'In Progress', 'Review', 'Done'],
        'custom_fields': [
            {'name': 'Priority', 'type': 'enum', 'options': ['P0', 'P1', 'P2', 'P3']},
            {'name': 'Effort', 'type': 'enum', 'options': ['Small', 'Medium', 'Large', 'XL']}
        ],
        'completion_rate': (0.60, 0.75)
    },
    'campaign': {
        'sections': ['Ideation', 'Planning', 'Creative', 'Execution', 'Review', 'Completed'],
        'custom_fields': [
            {'name': 'Campaign', 'type': 'enum', 'options': ['Q1 Launch', 'Product Update', 'Brand Awareness', 'Lead Gen']},
            {'name': 'Channel', 'type': 'enum', 'options': ['Social Media', 'Email', 'Content', 'Paid Ads', 'Events']},
            {'name': 'Budget', 'type': 'number'}
        ],
        'completion_rate': (0.75, 0.85)
    },
    'ongoing': {
        'sections': ['Requested', 'To Do', 'In Progress', 'Done'],
        'custom_fields': [
            {'name': 'Department', 'type': 'enum', 'options': ['Engineering', 'Marketing', 'Sales', 'Operations', 'Product']},
            {'name': 'Urgency', 'type': 'enum', 'options': ['Critical', 'High', 'Normal', 'Low']}
        ],
        'completion_rate': (0.40, 0.50)
    }
}

# Project type distribution by team type
PROJECT_TYPE_BY_TEAM = {
    'engineering': ['sprint', 'kanban'],
    'product': ['sprint', 'ongoing'],
    'marketing': ['campaign', 'ongoing'],
    'operations': ['kanban', 'ongoing'],
    'sales': ['kanban', 'ongoing']
}

# ============================================================================
# CONTENT GENERATION PATTERNS
# ============================================================================

# Task name patterns by team type
TASK_NAME_PATTERNS = {
    'engineering': [
        "{component} - {action} - {detail}",
        "Fix {bug_type} in {component}",
        "Implement {feature} for {component}",
        "Refactor {component} - {reason}"
    ],
    'marketing': [
        "{campaign} - {deliverable} - {platform}",
        "Create {asset_type} for {campaign}",
        "{channel} campaign - {action}",
        "Design {deliverable} for {target_audience}"
    ],
    'product': [
        "{feature} - {action}",
        "Research {topic} for {feature}",
        "Define requirements for {feature}",
        "User testing - {feature}"
    ],
    'operations': [
        "{process} - {action}",
        "Optimize {process}",
        "Setup {tool} for {department}",
        "Document {process}"
    ],
    'sales': [
        "{prospect_type} - {action}",
        "Follow up with {prospect}",
        "Prepare {deliverable} for {prospect}",
        "{action} for {deal_stage}"
    ]
}

# Description patterns
DESCRIPTION_PATTERNS = {
    'empty': 0.20,           # 20% tasks have no description
    'brief': 0.50,           # 50% have 1-3 sentences
    'detailed': 0.30         # 30% have detailed descriptions with bullets
}

# Comment patterns (based on "58% time spent on coordination")
COMMENTS_PER_TASK_MIN = 0
COMMENTS_PER_TASK_MAX = 8
ACTIVE_TASK_COMMENT_PROBABILITY = 0.60  # 60% of active tasks have comments

# Attachment patterns
ATTACHMENT_PROBABILITY = 0.25  # 25% of tasks have attachments
ATTACHMENTS_PER_TASK_MAX = 3

# Tag patterns
TAG_PROBABILITY = 0.40  # 40% of tasks have tags
TAGS_PER_TASK_MAX = 2

# ============================================================================
# WORKSPACE-LEVEL TAGS
# ============================================================================

COMMON_TAGS = [
    {'name': 'urgent', 'color': 'red'},
    {'name': 'blocked', 'color': 'red'},
    {'name': 'needs-review', 'color': 'orange'},
    {'name': 'bug', 'color': 'red'},
    {'name': 'enhancement', 'color': 'blue'},
    {'name': 'documentation', 'color': 'gray'},
    {'name': 'technical-debt', 'color': 'yellow'},
    {'name': 'customer-request', 'color': 'green'},
    {'name': 'quick-win', 'color': 'green'},
    {'name': 'research', 'color': 'purple'},
    {'name': 'dependencies', 'color': 'orange'},
    {'name': 'milestone', 'color': 'blue'},
    {'name': 'on-hold', 'color': 'gray'},
    {'name': 'high-priority', 'color': 'red'},
    {'name': 'low-priority', 'color': 'gray'}
]

# ============================================================================
# API CONFIGURATION
# ============================================================================

# Anthropic API (optional - for LLM-based content generation)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
USE_LLM_GENERATION = ANTHROPIC_API_KEY is not None

# LLM generation settings
LLM_MODEL = "claude-sonnet-4-20250514"
LLM_MAX_TOKENS = 1000
LLM_TEMPERATURE = 0.8  # Higher temperature for more variety

# ============================================================================
# FILE TYPE DISTRIBUTIONS
# ============================================================================

FILE_TYPES = {
    'engineering': ['pdf', 'doc', 'image', 'other'],  # Technical docs, diagrams
    'marketing': ['image', 'pdf', 'doc', 'other'],    # Images, presentations
    'product': ['pdf', 'doc', 'image', 'spreadsheet'],  # PRDs, research
    'operations': ['spreadsheet', 'pdf', 'doc', 'other'],
    'sales': ['pdf', 'doc', 'spreadsheet', 'other']
}

# ============================================================================
# TEMPORAL PATTERNS
# ============================================================================

# Activity patterns by day of week (more activity Mon-Wed)
ACTIVITY_BY_DAY = {
    0: 1.2,  # Monday - 20% more activity
    1: 1.2,  # Tuesday
    2: 1.1,  # Wednesday
    3: 0.9,  # Thursday - 10% less
    4: 0.8,  # Friday - 20% less
    5: 0.2,  # Saturday - minimal
    6: 0.2   # Sunday - minimal
}

# Weekend due date avoidance
AVOID_WEEKEND_DUE_DATES = 0.85  # 85% of tasks avoid weekend due dates

# Task completion time patterns (days after creation)
# Following log-normal distribution for realistic cycle times
COMPLETION_TIME_MEAN = 7      # Average 7 days
COMPLETION_TIME_STDDEV = 5    # Standard deviation 5 days

# ============================================================================
# VALIDATION RULES
# ============================================================================

# These ensure data quality and consistency
MAX_TASK_NAME_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
MAX_COMMENT_LENGTH = 1000
MIN_PROJECT_NAME_LENGTH = 5
MAX_PROJECT_NAME_LENGTH = 100

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"