CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    workspace_type TEXT DEFAULT 'organization',
    created_at TIMESTAMP NOT NULL,
    is_active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    team_type TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    is_archived BOOLEAN DEFAULT 0,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'member', 
    profile_photo_url TEXT,
    created_at TIMESTAMP NOT NULL,
    last_active TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);
CREATE TABLE IF NOT EXISTS team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(team_id, user_id)
);
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    project_type TEXT NOT NULL, 
    status TEXT DEFAULT 'active', 
    privacy TEXT DEFAULT 'team', 
    owner_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    start_date DATE,
    due_date DATE,
    completed_at TIMESTAMP,
    color TEXT DEFAULT 'light-gray', 
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    display_order INTEGER NOT NULL, 
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT ,
    parent_task_id TEXT,
    name TEXT NOT NULL,
    description TEXT, 
    assignee_id TEXT,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    modified_at TIMESTAMP,
    start_date DATE,
    due_date DATE,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    priority TEXT, 
    estimated_hours REAL,
    actual_hours REAL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    edited_at TIMESTAMP,
    is_edited BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT NOT NULL, 
    enum_options TEXT,
    is_required BOOLEAN DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS custom_field_values (
    value_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    value TEXT NOT NULL, 
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    UNIQUE(field_id, task_id) 
);
CREATE TABLE IF NOT EXISTS tags (
    tag_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT DEFAULT 'gray',
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id),
    UNIQUE(workspace_id, name)
);
CREATE TABLE IF NOT EXISTS task_tags (
    task_tag_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
    UNIQUE(task_id, tag_id)
);
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    uploaded_by TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER, 
    file_type TEXT,
    url TEXT, 
    uploaded_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);
