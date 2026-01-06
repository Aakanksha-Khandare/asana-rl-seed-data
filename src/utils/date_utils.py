"""
Date and time utility functions for generating realistic temporal patterns.
"""

import random
from datetime import datetime, timedelta
from src.config import (
    WORKSPACE_START_DATE,
    CURRENT_DATE,
    ACTIVITY_BY_DAY,
    AVOID_WEEKEND_DUE_DATES,
    COMPLETION_TIME_MEAN,
    COMPLETION_TIME_STDDEV,
    DUE_DATE_DISTRIBUTION
)


def generate_creation_date(start_date=None, end_date=None):
    """
    Generate a realistic creation date with weighted activity patterns.
    
    More activity on Mon-Wed, less on Thu-Fri, minimal on weekends.
    Higher activity in recent months (realistic growth pattern).
    
    Args:
        start_date: Start of date range (default: WORKSPACE_START_DATE)
        end_date: End of date range (default: CURRENT_DATE)
    
    Returns:
        datetime: A realistic creation timestamp
    """
    if start_date is None:
        start_date = WORKSPACE_START_DATE
    if end_date is None:
        end_date = CURRENT_DATE
    
    # Generate random date within range
    time_between = end_date - start_date
    days_between = time_between.days
    
    # Bias toward recent dates (more recent activity)
    # Use exponential distribution - more weight on recent dates
    random_days = int(random.expovariate(1.0 / (days_between / 2)))
    random_days = min(random_days, days_between)
    
    creation_date = start_date + timedelta(days=random_days)
    
    # Apply day-of-week weighting
    # If it's a weekend, shift to Friday or Monday
    while creation_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        if random.random() < 0.5:
            creation_date -= timedelta(days=1)  # Shift to Friday
        else:
            creation_date += timedelta(days=1)  # Shift to Monday
    
    # Add realistic time of day (9 AM - 6 PM work hours)
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    creation_date = creation_date.replace(hour=hour, minute=minute, second=second)
    
    return creation_date


def generate_due_date(created_at, project_type='sprint'):
    """
    Generate a realistic due date based on research patterns.
    
    Distribution (from research):
    - 25% within 1 week
    - 40% within 1 month  
    - 20% 1-3 months out
    - 10% no due date
    - 5% overdue
    
    Args:
        created_at: Task creation timestamp
        project_type: Type of project (affects due date patterns)
    
    Returns:
        datetime or None: Due date (None if no due date)
    """
    # Select distribution bucket
    rand = random.random()
    
    if rand < DUE_DATE_DISTRIBUTION['overdue']:
        # Overdue - due date in the past
        days_overdue = random.randint(1, 30)
        due_date = created_at - timedelta(days=days_overdue)
    
    elif rand < DUE_DATE_DISTRIBUTION['overdue'] + DUE_DATE_DISTRIBUTION['week_1']:
        # Due within 1 week
        days_ahead = random.randint(1, 7)
        due_date = created_at + timedelta(days=days_ahead)
    
    elif rand < DUE_DATE_DISTRIBUTION['overdue'] + DUE_DATE_DISTRIBUTION['week_1'] + DUE_DATE_DISTRIBUTION['month_1']:
        # Due within 1 month
        days_ahead = random.randint(8, 30)
        due_date = created_at + timedelta(days=days_ahead)
    
    elif rand < (DUE_DATE_DISTRIBUTION['overdue'] + DUE_DATE_DISTRIBUTION['week_1'] + 
                 DUE_DATE_DISTRIBUTION['month_1'] + DUE_DATE_DISTRIBUTION['months_1_3']):
        # Due in 1-3 months
        days_ahead = random.randint(31, 90)
        due_date = created_at + timedelta(days=days_ahead)
    
    else:
        # No due date
        return None
    
    # Avoid weekend due dates (85% of the time)
    if random.random() < AVOID_WEEKEND_DUE_DATES:
        due_date = avoid_weekend(due_date)
    
    # For sprint projects, align to sprint boundaries (2-week cycles)
    if project_type == 'sprint':
        due_date = align_to_sprint_boundary(due_date)
    
    return due_date


def avoid_weekend(date):
    """
    Shift a date to Friday if it falls on a weekend.
    
    Args:
        date: A datetime object
    
    Returns:
        datetime: Adjusted date (Friday if was weekend)
    """
    if date.weekday() == 5:  # Saturday
        return date - timedelta(days=1)  # Move to Friday
    elif date.weekday() == 6:  # Sunday
        return date - timedelta(days=2)  # Move to Friday
    return date


def align_to_sprint_boundary(date):
    """
    Align a date to the nearest sprint end (every 2 weeks).
    
    Engineering teams typically plan in 2-week sprints.
    
    Args:
        date: A datetime object
    
    Returns:
        datetime: Date aligned to sprint boundary
    """
    # Calculate days since workspace start
    days_since_start = (date - WORKSPACE_START_DATE).days
    
    # Find next sprint boundary (every 14 days)
    days_to_next_boundary = 14 - (days_since_start % 14)
    
    # If we're within 3 days of boundary, snap to it
    if days_to_next_boundary <= 3:
        return date + timedelta(days=days_to_next_boundary)
    
    return date


def generate_completion_date(created_at, due_date=None):
    """
    Generate a realistic completion date for a completed task.
    
    Uses log-normal distribution (realistic for cycle times).
    Most tasks complete in 3-10 days, some take longer.
    
    Args:
        created_at: When task was created
        due_date: Task due date (if any)
    
    Returns:
        datetime: Completion timestamp
    """
    # Generate days to complete using log-normal distribution
    # This creates realistic "cycle time" patterns
    days_to_complete = random.lognormvariate(
        mu=COMPLETION_TIME_MEAN / 3,  # Mean of underlying normal
        sigma=COMPLETION_TIME_STDDEV / 5  # Std dev of underlying normal
    )
    
    # Clip to reasonable range (1-30 days)
    days_to_complete = max(1, min(30, int(days_to_complete)))
    
    completed_at = created_at + timedelta(days=days_to_complete)
    
    # Ensure completion is before current date
    if completed_at > CURRENT_DATE:
        completed_at = CURRENT_DATE - timedelta(days=random.randint(1, 7))
    
    # If there's a due date, some tasks complete after (realistic!)
    if due_date:
        # 80% complete before due date, 20% complete after
        if random.random() < 0.8:
            # Complete before due date
            if completed_at > due_date:
                # Adjust to be before due date
                time_before_due = (due_date - created_at).total_seconds()
                random_seconds = random.uniform(0, time_before_due)
                completed_at = created_at + timedelta(seconds=random_seconds)
        # else: leave as-is (complete after due date - realistic!)
    
    # Add realistic time of day
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    completed_at = completed_at.replace(hour=hour, minute=minute, second=second)
    
    return completed_at


def is_business_day(date):
    """
    Check if a date is a business day (Mon-Fri).
    
    Args:
        date: A datetime object
    
    Returns:
        bool: True if weekday, False if weekend
    """
    return date.weekday() < 5  # 0-4 are Mon-Fri


def get_random_time_in_workday():
    """
    Generate a random time during work hours (9 AM - 6 PM).
    
    Returns:
        tuple: (hour, minute, second)
    """
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return (hour, minute, second)


def days_between(start_date, end_date):
    """
    Calculate number of days between two dates.
    
    Args:
        start_date: Start datetime
        end_date: End datetime
    
    Returns:
        int: Number of days
    """
    return (end_date - start_date).days