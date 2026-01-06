"""
Entry point for Asana seed data generation.
"""

from src.utils.db_utils import initialize_database
from src.generators.users import generate_users
from src.generators.projects import generate_projects
from src.generators.sections import generate_sections
from src.generators.teams import generate_teams
from src.generators.team_memberships import generate_team_memberships
from src.config import COMPANY_NAME


def main():
    print("Initializing database...")
    conn = initialize_database()
    cursor = conn.cursor()

    # -------------------------------------------------
    # WORKSPACE
    # -------------------------------------------------
    print("Creating workspace...")
    workspace_id = "workspace-001"

    cursor.execute(
        """
        INSERT INTO workspaces (workspace_id, name, domain, created_at, is_active)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, 1)
        """,
        (workspace_id, COMPANY_NAME, "example.com")
    )

    # -------------------------------------------------
    # USERS
    # -------------------------------------------------
    print("Generating users...")
    users = generate_users(workspace_id)

    for u in users:
        cursor.execute(
            """
            INSERT INTO users (user_id, workspace_id, name, email, role, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                u["user_id"],
                u["workspace_id"],
                u["name"],
                u["email"],
                u["role"],
                u["created_at"],
                u["is_active"],
            )
        )

    # -------------------------------------------------
    # TEAMS
    # -------------------------------------------------
    print("Generating teams...")
    teams = generate_teams(workspace_id)

    for t in teams:
        cursor.execute(
            """
            INSERT INTO teams (team_id, workspace_id, name, description, team_type, created_at, is_archived)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                t["team_id"],
                t["workspace_id"],
                t["name"],
                t["description"],
                t["team_type"],
                t["created_at"],
                t["is_archived"],
            )
        )

    # -------------------------------------------------
    # TEAM MEMBERSHIPS  (RUNS ONCE — ONLY HERE)
    # -------------------------------------------------
    print("Generating team memberships...")
    memberships = generate_team_memberships(users, teams)

    for m in memberships:
        cursor.execute(
            """
            INSERT INTO team_memberships (membership_id, team_id, user_id, joined_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                m["membership_id"],
                m["team_id"],
                m["user_id"],
                m["joined_at"],
            )
        )
    # -------------------------------------------------
    # PROJECTS
    # -------------------------------------------------
    
    print("Generating projects...")
    projects = generate_projects(workspace_id, teams, users)

    for p in projects:
        cursor.execute(
            """
            INSERT INTO projects (
                project_id, workspace_id, team_id, name, description,
                project_type, status, privacy, owner_id, created_at, color
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                p["project_id"],
                p["workspace_id"],
                p["team_id"],
                p["name"],
                p["description"],
                p["project_type"],
                p["status"],
                p["privacy"],
                p["owner_id"],
                p["created_at"],
                p["color"],
            )
        )

    # -------------------------------------------------
    # SECTIONS
    # -------------------------------------------------
    print("Generating sections...")
    sections = generate_sections(projects)

    for s in sections:
        cursor.execute(
            """
            INSERT INTO sections (section_id, project_id, name, display_order, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                s["section_id"],
                s["project_id"],
                s["name"],
                s["display_order"],
                s["created_at"],
            )
        )

    conn.commit()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()

