# Data Model: Parallel Task Execution

**Feature**: Parallel Task Execution
**Version**: 1.0
**Created**: 2026-04-01

---

## Overview

This document defines the data structures used for parallel task execution using Claude Code Team mode.

---

## Entities

### TeamMember

Represents an active Team Member agent executing a user story.

```python
class TeamMember:
    member_id: str           # "member-us1"
    story_id: str           # "US1"
    tasks: list[str]        # ["T010", "T011", "T012"]
    status: str             # "running" | "completed" | "failed" | "paused"
    checkpoint: str         # Last successful task ID
    spawned_at: str        # ISO timestamp
    completed_at: str | None  # ISO timestamp
```

**Status Transitions**:
- `running`: Member is actively executing tasks
- `completed`: All tasks finished successfully
- `failed`: Member crashed or all tasks failed
- `paused`: Conflict detected, waiting for manual resolution

---

### TeamConfig

Root configuration for a parallel execution session.

```python
class TeamConfig:
    team_name: str          # "sdd-002-parallel-task-{timestamp}"
    feature_dir: str        # Absolute path to feature directory
    created_at: str         # ISO timestamp
    status: str             # "active" | "completed" | "failed"
    max_members: int        # Maximum parallel members (default: 4)
    min_tasks_per_member: int  # Minimum tasks to spawn member (default: 3)
    members: list[TeamMember]
```

**Status Transitions**:
- `active`: Parallel execution in progress
- `completed`: All members finished successfully
- `failed`: One or more members failed

---

### TaskStatus

Represents the state of a single task as tracked in tasks.md.

```python
class TaskStatus:
    task_id: str            # "T010"
    status: str             # "pending" | "running" | "completed" | "failed"
    checked_by: str | None  # member_id that last modified
    modified_at: str        # ISO timestamp
```

**Status Transitions**:
- `pending`: Task not yet started (`- [ ]`)
- `running`: Task currently executing (`- [R]`)
- `completed`: Task finished successfully (`- [X]`)
- `failed`: Task failed (`- [-]`)

---

### Story

Represents a user story with its assigned tasks.

```python
class Story:
    story_id: str          # "US1"
    title: str             # "Automatic Parallelization"
    priority: str          # "P1" | "P2" | "P3" | "P4"
    tasks: list[str]        # ["T010", "T011", "T012"]
    status: str             # "pending" | "running" | "completed" | "failed"
```

---

## TeamConfig JSON Schema

File: `.specify/team-config.json` (runtime, gitignored)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TeamConfig",
  "type": "object",
  "required": ["team_name", "feature_dir", "created_at", "status", "members"],
  "properties": {
    "team_name": {
      "type": "string",
      "pattern": "^sdd-002-parallel-task-\\d+$"
    },
    "feature_dir": {
      "type": "string"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "enum": ["active", "completed", "failed"]
    },
    "max_members": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4,
      "default": 4
    },
    "min_tasks_per_member": {
      "type": "integer",
      "minimum": 1,
      "default": 3
    },
    "members": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/TeamMember"
      }
    }
  },
  "definitions": {
    "TeamMember": {
      "type": "object",
      "required": ["member_id", "story_id", "tasks", "status", "checkpoint"],
      "properties": {
        "member_id": {
          "type": "string",
          "pattern": "^member-[a-z0-9]+$"
        },
        "story_id": {
          "type": "string",
          "pattern": "^US[0-9]+$"
        },
        "tasks": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^T[0-9]+$"
          }
        },
        "status": {
          "type": "string",
          "enum": ["running", "completed", "failed", "paused"]
        },
        "checkpoint": {
          "type": "string",
          "pattern": "^T[0-9]+$"
        },
        "spawned_at": {
          "type": "string",
          "format": "date-time"
        },
        "completed_at": {
          "type": ["string", "null"],
          "format": "date-time"
        }
      }
    }
  }
}
```

---

## Tasks.md Checkbox Format

The tasks.md file uses checkbox notation:

| Symbol | Meaning | Markdown |
|--------|---------|----------|
| Pending | Not started | `- [ ]` |
| Running | Currently executing | `- [R]` |
| Completed | Successfully finished | `- [X]` |
| Failed | Task failed | `- [-]` |

Example tasks.md excerpt:

```markdown
## Phase 3: User Story 1

- [ ] T009 [P] [US1] First task for US1
- [R] T010 [US1] Second task (running)
- [X] T011 [US1] Third task (completed)
- [-] T012 [US1] Fourth task (failed)
```

---

## File Locations

| File | Purpose | Git Tracked |
|------|--------|-------------|
| `.specify/team-config.json` | Runtime team state | No (gitignored) |
| `tasks.md` | Task list with status | Yes |
| `specs/002-parallel-task-execution/tasks.md` | Feature spec tasks | Yes |

---

## Constraints

From spec.md:

- **FR-007**: Maximum 4 parallel Team Members
- **FR-008**: Minimum 3 tasks per member before spawning
- **FR-009**: Auto-fallback to sequential when Team mode unavailable
- **A5**: Designed for 2-4 parallel stories
