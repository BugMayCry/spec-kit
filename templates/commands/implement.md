---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc*or eslint.config.* exists → create/verify .eslintignore
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. **Parallel Execution Detection** (NEW - for features with 2+ independent user stories):

   Check if parallel execution should be used:

   a. **Detect CLI flags**:
      - `--serial`: Force sequential execution, skip to step 6b
      - `--parallel`: Force parallel execution

   b. **Check Team mode availability**:
      ```python
      import os
      team_mode_enabled = os.getenv("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"
      ```

   c. **Analyze parallel opportunities** (if not --serial and team mode available):
      - Parse tasks.md for story markers [US1], [US2], etc.
      - Identify stories with 3+ tasks each (FR-008: min tasks per member)
      - Check for [P] parallelizable tasks within each story
      - Limit to max 4 parallel members (FR-007)

   d. **Decision flow**:
      - If `--serial` set: Use sequential execution
      - If `--parallel` set: Use parallel execution (even with 1 story)
      - If team mode unavailable: Fall back to sequential, warn user (EC-001)
      - If 2+ stories with 3+ tasks each: Use parallel execution
      - Otherwise: Use sequential execution

   e. **If parallel execution selected**:
      - Create `.specify/team-config.json` with team configuration
      - Spawn Team Members for each parallel story
      - Monitor progress via SendMessage
      - Handle failures per EC-002 through EC-005
      - Skip to step 10 after parallel execution completes

   f. **Helper Functions for Parallel Execution**:

      ```python
      # --- T004: Parallel Detection ---
      def analyze_parallel_opportunities(tasks_md: Path) -> list[Story]:
          """Analyze tasks.md for parallelizable user stories.
          Returns list of Story objects with 3+ tasks each.
          """
          # Parse tasks.md for [US1], [US2], etc. markers
          # Count tasks per story
          # Filter to stories with 3+ tasks (FR-008)
          # Return list of parallelizable stories

      # --- T005: TeamConfig Entity Classes ---
      class TeamMember:
          member_id: str
          story_id: str
          tasks: list[str]
          status: str  # running | completed | failed | paused
          checkpoint: str

      class TeamConfig:
          team_name: str
          feature_dir: str
          created_at: str
          status: str  # active | completed | failed
          members: list[TeamMember]

      def load_team_config(path: Path) -> TeamConfig:
          """Load team-config.json if exists."""
          # JSON deserialize

      def save_team_config(config: TeamConfig, path: Path) -> None:
          """Save team-config.json."""
          # JSON serialize

      # --- T006: Git Force-with-Lease Sync ---
      def sync_tasks_md(repo_path: Path, tasks_md_path: Path) -> bool:
          """Sync tasks.md with origin using force-with-lease.
          Returns True if sync succeeded, False if conflict.
          Implements retry logic (2 retries on failure).
          """
          # git fetch origin
          # git rebase origin/main
          # git add tasks_md_path
          # git commit -m "Update tasks.md"
          # git push --force-with-lease origin HEAD
          # On conflict: retry up to 2 times

      # --- T007: CLI Flag Handlers ---
      def parse_implement_flags(arguments: str) -> dict:
          """Parse --serial and --parallel flags from arguments.
          Returns dict with 'serial' and 'parallel' boolean flags.
          """
          # Parse arguments string for flags

      # --- T008: Team Mode Availability ---
      def is_team_mode_available() -> bool:
          """Check if CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is set.
          Returns True if Team mode is enabled.
          """
          import os
          return os.getenv("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"

      # --- T009: Spawn Team Members ---
      def spawn_team_members(stories: list[Story], config: TeamConfig) -> list[Agent]:
          """Spawn Team Member agents for each story using Agent tool.
          Uses Agent tool with team_name and name parameters.
          Creates member-{story-id} naming convention.
          Enforces max 4 members (FR-007) and min 3 tasks (FR-008).
          """
          # Use Agent tool:
          # agent = Agent(
          #     team_name=config.team_name,
          #     name=f"member-{story.story_id.lower()}",
          #     ...,
          # )
          # Track spawned members in config.members

      # --- T010: Monitor Progress ---
      def monitor_progress(members: list[Agent], config: TeamConfig) -> None:
          """Monitor and aggregate progress from all Team Members.
          Track task start/complete/fail events.
          Update team-config.json with member status.
          Display aggregated metrics view (SC-007).
          """
          # Listen for progress messages via SendMessage
          # Aggregate progress from all members
          # Update task checkboxes in tasks.md
          # Display real-time metrics

      # --- T011: Team Lead → Member Communication ---
      def send_assign_message(member: Agent, story: Story, tasks: list[str]) -> None:
          """Send assign message to Team Member with task list.
          Message format per contracts/team-protocol.md:
          {
            "type": "assign",
            "member_id": "member-us1",
            "tasks": ["T010", "T011", "T012"],
            "feature_dir": "...",
            "tasks_md": "..."
          }
          """
          # Use SendMessage tool with structured JSON

      def handle_progress_message(message: dict) -> None:
          """Handle progress message from Team Member.
          Update task status in tasks.md.
          Handle errors per EC-002 through EC-005.
          """
          # Parse message type
          # Update task checkbox: running [R], completed [X], failed [-]
          # Log event

      def handle_complete_message(message: dict) -> None:
          """Handle complete message from Team Member.
          Mark member as completed in config.
          Check if all members done.
          """
          # Update member status in config
          # If all complete, transition to step 10

      # --- Edge Case Handlers (EC-002 through EC-005) ---
      def handle_git_push_failure(member_id: str, error: str) -> None:
          """EC-002: Git push failure handling.
          Retry fetch + rebase + push up to 2 times.
          If still failing due to merge conflict, pause branch.
          Notify Team Lead to resolve manually.
          """
          # Retry logic with counter
          # On persistent conflict: mark member as "paused"

      def handle_member_crash(member_id: str) -> None:
          """EC-003: Member crash recovery.
          Detect member failure via missing progress messages.
          Respawn new Member from last successful checkpoint.
          """
          # Find checkpoint from config
          # Respawn member with same member_id
          # Resume from checkpoint task

      def handle_resource_insufficient() -> None:
          """EC-004: Resource insufficient warning.
          Display warning suggesting --serial flag.
          Continue with available resources if possible.
          """
          # Display warning message
          # Suggest --serial flag

      def handle_manual_edit_conflict(member_id: str) -> None:
          """EC-005: Manual edit conflict detection.
          Detect conflict on next push via force-with-lease.
          Pause affected branch, prompt user to resolve manually.
          """
          # Mark member as "paused"
          # Prompt user to resolve conflict

      # --- T013: Structured Logging ---
      def log_team_event(event_type: str, member_id: str, details: dict) -> None:
          """T013: Structured logging for key events.
          Log Team Member spawn events (SC-006).
          Log task start/complete/fail events.
          Log push sync status and error conditions.
          Uses structured format for log aggregation.
          """
          import json
          from datetime import datetime
          log_entry = {
              "timestamp": datetime.utcnow().isoformat(),
              "event_type": event_type,  # spawn, task_start, task_complete, task_fail, push, error
              "member_id": member_id,
              **details
          }
          # Log to structured logger (e.g., JSON to stdout or file)
          print(f"[TEAM] {json.dumps(log_entry)}")

      # --- T014: Aggregated Metrics View ---
      def display_metrics_view(config: TeamConfig, all_tasks: dict) -> None:
          """T014: Display aggregated metrics view.
          Show total tasks, completed, failed, running, pending per story (SC-007).
          Show per-user story status with member breakdown.
          Uses Rich library for terminal output formatting.
          """
          from rich.table import Table
          from rich.console import Console

          console = Console()
          table = Table(title="Parallel Execution Progress")

          # Add columns: Story, Total, Completed, Failed, Running, Pending, Member
          table.add_column("Story", style="cyan")
          table.add_column("Total", justify="right", style="white")
          table.add_column("Completed", justify="right", style="green")
          table.add_column("Failed", justify="right", style="red")
          table.add_column("Running", justify="right", style="yellow")
          table.add_column("Pending", justify="right", style="dim")
          table.add_column("Member", style="magenta")

          # Aggregate metrics per story
          for member in config.members:
              story_id = member.story_id
              tasks = member.tasks
              completed = sum(1 for t in tasks if all_tasks.get(t) == "completed")
              failed = sum(1 for t in tasks if all_tasks.get(t) == "failed")
              running = sum(1 for t in tasks if all_tasks.get(t) == "running")
              pending = len(tasks) - completed - failed - running

              table.add_row(
                  story_id,
                  str(len(tasks)),
                  str(completed),
                  str(failed),
                  str(running),
                  str(pending),
                  member.member_id
              )

          console.print(table)

      # --- T015: Real-time Progress Display ---
      def update_progress_display(member_id: str, task_id: str, status: str) -> None:
          """T015: Update real-time progress display.
          Show running tasks with [R] marker in aggregated view.
          Update display on each progress message.
          Handle concurrent output from multiple members.
          """
          # Update the metrics view with new status
          # Use Rich Live display for real-time updates
          # Show [R] for running, [X] for completed, [-] for failed
          status_symbols = {
              "running": "[R]",
              "completed": "[X]",
              "failed": "[-]",
              "pending": "[ ]"
          }
          print(f"  {status_symbols.get(status, '[?]')} {task_id} ({member_id})")

      # --- T012: Integrate Team Spawning into Execution Flow ---
      def execute_with_parallelism(stories: list[Story], tasks_md: Path) -> None:
          """Main parallel execution orchestrator.
          1. Execute Phase 1-2 sequentially (Team Lead)
          2. Spawn Team Members for Phase 3+ stories
          3. Monitor and aggregate progress
          4. Handle graceful degradation
          """
          # Phase 1-2: Sequential execution by Team Lead
          # Phase 3+: Parallel Team Member execution
          # Enforce 4 member max (FR-007)
          # Enforce 3 task min per member (FR-008)
      ```

6b. **Sequential Execution** (fallback):
   - Execute tasks in phase order as defined in step 6
   - Skip parallel detection and Team spawning
   - Process tasks sequentially as in original implement.md behavior

7. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

8. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

9. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

10. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/speckit.tasks` first to regenerate the task list.

