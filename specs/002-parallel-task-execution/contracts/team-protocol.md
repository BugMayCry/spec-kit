# Team Communication Protocol

**Feature**: Parallel Task Execution
**Version**: 1.0
**Created**: 2026-04-01

---

## Overview

This protocol defines the communication patterns between Team Lead and Team Members when executing parallel user story implementation.

---

## Message Types

### 1. assign (Team Lead → Member)

Sent by Team Lead to assign a set of tasks to a Team Member.

```json
{
  "type": "assign",
  "member_id": "member-us1",
  "story_id": "US1",
  "tasks": ["T010", "T011", "T012"],
  "feature_dir": "/path/to/specs/002-parallel-task-execution",
  "tasks_md": "/path/to/tasks.md",
  "team_config": "/path/to/.specify/team-config.json"
}
```

**Fields**:
- `type`: Always "assign"
- `member_id`: Unique member identifier (format: "member-{story-id}")
- `story_id`: User story being assigned (e.g., "US1")
- `tasks`: List of task IDs assigned to this member
- `feature_dir`: Absolute path to feature directory
- `tasks_md`: Absolute path to tasks.md file
- `team_config`: Absolute path to team-config.json

**Response**: Member acknowledges with `progress` message for first task

---

### 2. progress (Member → Team Lead)

Sent by Member to report task status changes.

```json
{
  "type": "progress",
  "member_id": "member-us1",
  "story_id": "US1",
  "task_id": "T010",
  "status": "completed",
  "error": null
}
```

```json
{
  "type": "progress",
  "member_id": "member-us1",
  "story_id": "US1",
  "task_id": "T011",
  "status": "failed",
  "error": "File conflict on tasks.md line 42"
}
```

**Status Values**:
- `running`: Task has started execution
- `completed`: Task finished successfully
- `failed`: Task encountered an error
- `skipped`: Task was skipped (e.g., dependency failed)

**Fields**:
- `type`: Always "progress"
- `member_id`: Member identifier
- `story_id`: User story ID
- `task_id`: Task ID being reported
- `status`: One of running/completed/failed/skipped
- `error`: Error message string if status is "failed", null otherwise

---

### 3. complete (Member → Team Lead)

Sent by Member when all assigned tasks are done.

```json
{
  "type": "complete",
  "member_id": "member-us1",
  "story_id": "US1",
  "completed_all": true,
  "summary": {
    "completed": 5,
    "failed": 0,
    "skipped": 1
  },
  "final_checkpoint": "T015"
}
```

**Fields**:
- `type`: Always "complete"
- `member_id`: Member identifier
- `story_id`: User story ID
- `completed_all`: true if all tasks completed, false if some failed/skipped
- `summary`: Count of each task status
- `final_checkpoint`: Last successfully completed task ID

---

### 4. spawn (Team Lead internal)

Internal message used when spawning a new Team Member agent.

```json
{
  "type": "spawn",
  "member_id": "member-us1",
  "story_id": "US1",
  "agent_name": "member-us1"
}
```

**Fields**:
- `type`: Always "spawn"
- `member_id`: Member identifier
- `story_id`: User story ID
- `agent_name`: Name for the spawned Agent

---

## TeamConfig File

Runtime state stored in `.specify/team-config.json`:

```json
{
  "team_name": "sdd-002-parallel-task",
  "feature_dir": "/path/to/specs/002-parallel-task-execution",
  "created_at": "2026-04-01T12:00:00Z",
  "status": "active",
  "members": [
    {
      "member_id": "member-us1",
      "story_id": "US1",
      "tasks": ["T010", "T011", "T012"],
      "status": "running",
      "checkpoint": "T010"
    }
  ]
}
```

---

## Error Handling

### EC-002: Git Push Failure

When Git push fails, Member sends:

```json
{
  "type": "progress",
  "member_id": "member-us1",
  "story_id": "US1",
  "task_id": "T012",
  "status": "failed",
  "error": "Git push failed: conflict on tasks.md"
}
```

Team Lead should then pause that branch and notify user.

### EC-003: Member Crash

When Team Lead detects Member failure (via missing progress messages):

1. Mark member status as "failed"
2. Respawn new Member with same member_id
3. New Member resumes from checkpoint task

---

## Sync Protocol

### Git Force-with-Lease Flow

1. **Before starting task**: Member fetches origin and rebases local changes
2. **After completing task**: Member runs:
   ```bash
   git fetch origin
   git rebase origin/main
   git add tasks.md
   git commit -m "Update tasks.md"
   git push --force-with-lease origin HEAD
   ```
3. **On conflict**: Retry up to 2 times, then pause and notify Team Lead
