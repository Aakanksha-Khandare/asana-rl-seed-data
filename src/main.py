"""
Entry point for Asana seed data generation.
"""

from src.utils.db_utils import initialize_database
from src.generators.users import generate_users
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

    conn.commit()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()

