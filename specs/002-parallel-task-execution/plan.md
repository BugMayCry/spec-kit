# Implementation Plan: Parallel Task Execution

**Branch**: `002-parallel-task-execution` | **Date**: 2026-04-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `./spec.md`

---

## Summary

Extend `/speckit.implement` to automatically parallelize execution of independent user stories using Claude Code Team mode. Team Lead executes Phase 1-2 sequentially, then spawns Team Members for parallel story execution. Feature maintains backward compatibility and gracefully degrades to sequential execution when parallel conditions are not met.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, httpx, Agent tool (for Team mode spawning), GitPython (for force-with-lease)
**Storage**: JSON files (team-config.json), tasks.md (Git-tracked)
**Testing**: pytest
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: CLI tool - modifying existing `templates/commands/implement.md`
**Performance Goals**:
- Team Member spawn time < 5 seconds
- 40-60% faster execution for 2+ parallel stories
- Backward compatibility maintained

**Constraints**:
- Maximum 4 parallel Team Members
- Minimum 3 tasks per Member to spawn
- Must fallback to sequential if Team mode unavailable

**Scale/Scope**:
- 2-4 parallel user stories supported
- Single Session execution (no cross-Session recovery)

---

## Constitution Check

*Note: Constitution.md is still a template with placeholders. No gates to evaluate.*

---

## Project Structure

### Documentation (this feature)

```text
specs/002-parallel-task-execution/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: Technology research
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Quick start guide
├── contracts/           # Phase 1: Interface contracts
│   └── team-protocol.md
└── tasks.md            # Phase 2: Task breakdown (/speckit.tasks)
```

### Source Code (modifying existing templates)

```text
templates/commands/
└── implement.md         # MODIFIED: Add parallel execution logic

.specify/
├── team-config.json    # CREATED: Team member tracking (runtime, gitignored)
└── memory/
    └── constitution.md   # Existing
```

---

## Research: Claude Code Team Mode Integration

### Decision: How to spawn Team Members

**Choice**: Use Agent tool with `team_name` and `name` parameters

**Rationale**:
- Agent tool natively supports Team mode
- No manual process spawning required
- Automatic message routing via team_name
- Members can be named uniquely (member-us1, member-us2)

**Alternative rejected**: Manual subprocess spawning
- Would require manual message queue management
- No native SendMessage support

### Decision: How to detect Team mode availability

**Choice**: Check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable

**Rationale**:
- Standard env var for Team mode feature flag
- Easy to check before attempting spawn
- Allows graceful fallback per EC-001

### Decision: How to communicate between Team Lead and Members

**Choice**: Use SendMessage tool with structured JSON messages

**Message Types**:
- `assign`: Team Lead → Member (task assignment)
- `progress`: Member → Team Lead (task status update)
- `complete`: Member → Team Lead (all tasks done)

### Decision: How to sync tasks.md across Members

**Choice**: Git force-with-lease with retry logic

**Flow**:
1. Member completes task
2. fetch origin tasks.md
3. rebase local changes
4. push --force-with-lease
5. If fails → retry 2x, then pause branch

---

## Phase 0: Research

### 0.1 Team Mode API Research

**Topic**: Claude Code Team mode capabilities and limitations
**Research**:
- How to spawn agents with Agent tool
- How to use SendMessage/TaskUpdate
- Team name conventions
- Member lifecycle management

### 0.2 Git Synchronization Research

**Topic**: Git force-with-lease patterns for concurrent file editing
**Research**:
- Python Git library (GitPython) force-with-lease usage
- Conflict detection strategies
- Rebase vs merge for tasks.md

### 0.3 Progress Tracking Research

**Topic**: Real-time aggregation view patterns
**Research**:
- How to aggregate progress from multiple agents
- Terminal output strategies for parallel progress
- Structured logging format

---

## Phase 1: Design

### 1.1 Data Model

#### TeamConfig Entity

```python
class TeamMember:
    member_id: str           # "member-us1"
    story_id: str           # "US1"
    tasks: list[str]        # ["T010", "T011", "T012"]
    status: str             # "running" | "completed" | "failed"
    checkpoint: str         # Last successful task ID

class TeamConfig:
    team_name: str          # "sdd-002-parallel-task"
    feature_dir: str        # Absolute path
    created_at: str         # ISO timestamp
    status: str             # "active" | "completed" | "failed"
    members: list[TeamMember]
```

#### TaskStatus Entity

```python
class TaskStatus:
    task_id: str            # "T010"
    status: str             # "pending" | "running" | "completed" | "failed"
    checked_by: str | None  # member_id that last modified
    modified_at: str        # ISO timestamp
```

### 1.2 Contracts

#### Team Communication Protocol

**assign** (Team Lead → Member):
```json
{
  "type": "assign",
  "member_id": "member-us1",
  "tasks": ["T010", "T011", "T012"],
  "feature_dir": "/path/to/specs/002-parallel-task-execution",
  "tasks_md": "/path/to/tasks.md"
}
```

**progress** (Member → Team Lead):
```json
{
  "type": "progress",
  "member_id": "member-us1",
  "task_id": "T010",
  "status": "completed",
  "error": null
}
```

**complete** (Member → Team Lead):
```json
{
  "type": "complete",
  "member_id": "member-us1",
  "completed_all": true,
  "summary": {
    "completed": 5,
    "failed": 0,
    "skipped": 1
  }
}
```

### 1.3 Quickstart

**For Testing Parallel Execution**:
1. Create feature with 2+ independent user stories
2. Run `/speckit.implement`
3. Observe parallel task execution
4. Monitor progress aggregation view

---

## Implementation Details

### File Changes

| File | Action | Description |
|------|--------|-------------|
| `templates/commands/implement.md` | Modify | Add parallel detection and Team spawning |
| `.specify/team-config.json` | Create | Runtime team state (gitignored) |
| `specs/002-parallel-task-execution/contracts/team-protocol.md` | Create | Protocol documentation |

### Key Functions to Add

```python
# implement.md additions

def analyze_parallel_opportunities(tasks_md: Path) -> list[Story]:
    """Analyze tasks.md for parallelizable user stories."""

def spawn_team_members(stories: list[Story], config: TeamConfig) -> list[Agent]:
    """Spawn Team Members for each story."""

def monitor_progress(members: list[Agent], config: TeamConfig) -> None:
    """Monitor and aggregate progress from all Members."""

def handle_team_mode_unavailable() -> None:
    """Fallback to sequential execution."""
```

### Parameters

| Flag | Behavior |
|------|----------|
| `--serial` | Force sequential execution |
| `--parallel` | Force parallel execution (even with 1 story) |

---

## Complexity Tracking

No constitution violations to justify - all decisions follow principles of simplicity and observability.

---

## Testing Strategy

### Unit Tests
- `test_parallel_detection.py`: Test story parallelization logic
- `test_team_config.py`: Test TeamConfig serialization
- `test_git_sync.py`: Test force-with-lease behavior

### Integration Tests
- Mock Team mode environment
- Test full parallel execution flow
- Test fallback behavior

---

## Rollout Plan

1. **Phase 1**: Modify implement.md with parallel detection (no Team mode yet)
2. **Phase 2**: Add Team spawning with mock Members
3. **Phase 3**: Add real Team mode integration
4. **Phase 4**: Add observability and progress tracking
5. **Phase 5**: Testing and refinement
