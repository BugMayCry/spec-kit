# Tasks: Parallel Task Execution

**Input**: Design documents from `/specs/002-parallel-task-execution/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Prepare implement.md for parallel execution modifications

- [X] T001 Create team-protocol.md contract in specs/002-parallel-task-execution/contracts/team-protocol.md
- [X] T002 Create TeamConfig data model in data-model.md (TeamMember, TeamConfig, TaskStatus entities)
- [X] T003 Create .specify/team-config.json schema documentation

---

## Phase 2: Foundational (Core Parallel Infrastructure)

**Purpose**: Core infrastructure that enables parallel execution without actual Team mode

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Implement parallel detection function in templates/commands/implement.md
  - Add `analyze_parallel_opportunities(tasks_md: Path) -> list[Story]` function
  - Parse tasks.md for [P] markers and story assignments
  - Detect independent stories that can run in parallel
- [X] T005 [P] Implement TeamConfig entity classes
  - Add TeamMember, TeamConfig, TaskStatus data classes
  - Add JSON serialization/deserialization for team-config.json
- [X] T006 [P] Implement Git force-with-lease sync function
  - Add `sync_tasks_md()` function using GitPython
  - Implement fetch → rebase → push --force-with-lease flow
  - Add retry logic (2 retries on failure)
- [X] T007 Add --serial and --parallel flag handlers
  - Add CLI flag parsing for serial/parallel mode selection
  - Store flag state for execution decisions
- [X] T008 Add team mode availability detection
  - Check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable
  - Implement fallback to sequential when Team mode unavailable (EC-001)

**Checkpoint**: Foundation ready - parallel infrastructure exists but Team mode not yet active

---

## Phase 3: User Story 1 - Automatic Parallelization (Priority: P1) 🎯 MVP

**Goal**: Enable parallel execution of independent user stories using Claude Code Team mode

**Independent Test**: Create a feature with 2+ independent user stories, run `/speckit.implement`, verify multiple stories are implemented concurrently

### Implementation for User Story 1

- [X] T009 [P] [US1] Implement `spawn_team_members()` function in templates/commands/implement.md
  - Use Agent tool with `team_name` and `name` parameters
  - Create member-{story-id} naming convention
  - Implement member lifecycle management
- [X] T010 [P] [US1] Implement `monitor_progress()` function
  - Track task start/complete/fail events
  - Aggregate progress from all team members
  - Update team-config.json with member status
- [X] T011 [US1] Implement Team Lead → Member communication protocol
  - Send `assign` message with task list to each member
  - Handle `progress` messages from members
  - Handle `complete` messages from members
- [X] T012 [US1] Integrate Team spawning into implement.md execution flow
  - Execute Phase 1-2 sequentially by Team Lead
  - Spawn Team Members for Phase 3+ parallel execution
  - Enforce 4 member maximum limit (FR-007)
  - Enforce 3 task minimum per member (FR-008)

**Checkpoint**: At this point, User Story 1 should be functional - parallel execution works with Team mode

---

## Phase 4: User Story 2 - Transparent Progress Tracking (Priority: P2)

**Goal**: Provide clear progress visibility during parallel execution

**Independent Test**: Monitor output during parallel execution, verify progress updates for each parallel task

### Implementation for User Story 2

- [X] T013 [P] [US2] Add structured logging for key events in templates/commands/implement.md
  - Log Team Member spawn events
  - Log task start/complete/fail events (SC-006)
  - Log push sync status and error conditions
- [X] T014 [P] [US2] Implement aggregated metrics view
  - Display total tasks, completed, failed, running, pending per story (SC-007)
  - Show per-user story status with member breakdown
  - Use Rich library for terminal output formatting
- [X] T015 [US2] Implement real-time progress display
  - Show running tasks with [R] marker in aggregated view
  - Update display on each progress message
  - Handle concurrent output from multiple members

**Checkpoint**: At this point, User Story 2 should be functional - progress tracking is visible

---

## Phase 5: User Story 3 - Graceful Degradation (Priority: P3)

**Goal**: Handle failures gracefully so partial completion is still valuable

**Independent Test**: Introduce failure in one parallel branch, verify others complete successfully

### Implementation for User Story 3

- [X] T016 [P] [US3] Implement EC-002: Git push failure handling
  - Retry fetch + rebase + push up to 2 times
  - If still failing due to merge conflict, pause branch
  - Notify Team Lead to resolve manually
- [X] T017 [P] [US3] Implement EC-003: Member crash recovery
  - Detect member failure via missing progress messages
  - Respawn new Member from last successful checkpoint
  - Resume member from checkpoint task ID
- [X] T018 [US3] Implement EC-004: Resource insufficient warning
  - Display warning when resources limited
  - Suggest --serial flag as alternative
  - Continue with available resources if possible
- [X] T019 [US3] Implement EC-005: Manual edit conflict detection
  - Detect conflict on next push via force-with-lease
  - Pause affected branch on conflict
  - Prompt user to resolve manually

**Checkpoint**: At this point, User Story 3 should be functional - failures are handled gracefully

---

## Phase 6: User Story 4 - Manual Override Controls (Priority: P4)

**Goal**: Provide escape hatches for debugging, CI/CD, or user preference

**Independent Test**: Run with --serial and --parallel flags, verify expected behavior

### Implementation for User Story 4

- [X] T020 [P] [US4] Verify --serial flag forces sequential execution
  - When --serial is set, execute all tasks sequentially
  - Skip Team spawning entirely
  - No parallel overhead regardless of story count
- [X] T021 [P] [US4] Verify --parallel flag forces parallel execution
  - When --parallel is set with single story, spawn Team anyway
  - Force parallel mode even with one story
  - Useful for testing or CI/CD scenarios

**Checkpoint**: At this point, User Story 4 should be functional - manual controls work

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T022 [P] Add unit tests for parallel detection logic in tests/test_parallel_detection.py
- [X] T023 [P] Add unit tests for TeamConfig serialization in tests/test_team_config.py
- [X] T024 [P] Add unit tests for Git sync behavior in tests/test_git_sync.py
- [X] T025 Add integration tests for full parallel execution flow
  - Mock Team mode environment
  - Test fallback behavior (EC-001)
- [X] T026 Verify backward compatibility (SC-005)
  - Existing sequential behavior unchanged when parallel conditions not met
  - Test single story scenario without parallel overhead
- [X] T027 Add .specify/team-config.json to .gitignore
- [X] T028 Update implement.md with parallel execution documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1 (progress tracking is independent)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2 (graceful degradation is independent)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (manual controls are independent)

### Within Each User Story

- Core infrastructure before integration
- Foundational tasks before user story tasks
- US1 complete before parallel testing can be fully validated

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel
- All tasks for a user story marked [P] can run in parallel
- US2, US3, US4 are independent and can be implemented in parallel by different agents

---

## Parallel Example: User Story 1

```bash
# Launch all foundational tasks together:
Task: T004 - Implement parallel detection function
Task: T005 - Implement TeamConfig entity classes
Task: T006 - Implement Git force-with-lease sync
Task: T007 - Add --serial and --parallel flag handlers

# Launch US1 implementation tasks:
Task: T009 - Implement spawn_team_members()
Task: T010 - Implement monitor_progress()

# Launch US2, US3, US4 tasks in parallel after foundational:
Task: T013, T016, T020 - First tasks of US2, US3, US4
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test parallel execution works
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Polish → Final validation

### Rollout Plan (From plan.md)

1. **Phase 1**: Modify implement.md with parallel detection (no Team mode yet)
2. **Phase 2**: Add Team spawning with mock Members
3. **Phase 3**: Add real Team mode integration
4. **Phase 4**: Add observability and progress tracking
5. **Phase 5**: Testing and refinement

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Rollout plan maps to task phases: Phase 1-2 of rollout → Phase 2 of tasks (Foundational)
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are OPTIONAL for this feature - no explicit test request in spec
