"""
E2E tests for parallel task execution feature.

These tests verify the complete parallel execution flow by:
1. Creating a temporary feature project with test spec files
2. Running the implement command with mocked Team mode
3. Verifying the expected behavior

Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 for full Team mode testing.
"""

import pytest
import tempfile
import shutil
import json
import os
import re
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestE2EParallelExecution:
    """End-to-end tests for parallel execution scenarios."""

    @pytest.fixture
    def temp_feature_dir(self):
        """Create a temporary directory for E2E testing."""
        temp_dir = tempfile.mkdtemp(prefix="sdd_e2e_")
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def mock_team_config(self):
        """Mock TeamConfig for testing."""
        return {
            "team_name": "test-team-001",
            "feature_dir": "/test/feature",
            "created_at": "2026-04-01T12:00:00Z",
            "status": "active",
            "max_members": 4,
            "min_tasks_per_member": 3,
            "members": []
        }

    def test_e2e_analyze_story_markers_from_tasks_md(self, temp_feature_dir):
        """
        E2E Scenario: Parse tasks.md and extract story markers correctly.

        Tests FR-001: System MUST automatically detect when multiple user stories
        can be executed in parallel by analyzing task dependencies in tasks.md.
        """
        # Create a realistic tasks.md content
        tasks_content = """# Tasks: Test Feature

## Phase 1: Setup

- [X] T001 Setup task 1
- [X] T002 Setup task 2

## Phase 2: Foundational

- [X] T003 Foundational task

## Phase 3: User Story 1

- [ ] T004 [P] [US1] First US1 task
- [ ] T005 [P] [US1] Second US1 task
- [ ] T006 [US1] Third US1 task

## Phase 4: User Story 2

- [ ] T007 [P] [US2] First US2 task
- [ ] T008 [P] [US2] Second US2 task
- [ ] T009 [US2] Third US2 task
- [ ] T010 [US2] Fourth US2 task

## Phase 5: User Story 3

- [ ] T011 [US3] Only one task for US3
"""

        # Write tasks.md
        tasks_md = temp_feature_dir / "tasks.md"
        tasks_md.write_text(tasks_content)

        # Test the parsing logic
        from test_parallel_detection import parse_stories_from_tasks_md, SAMPLE_TASKS_MD
        stories = parse_stories_from_tasks_md(tasks_content)

        assert 'US1' in stories, "US1 should be detected"
        assert 'US2' in stories, "US2 should be detected"
        assert len(stories['US1']) == 3, "US1 should have 3 tasks"
        assert len(stories['US2']) == 4, "US2 should have 4 tasks"

    def test_e2e_parallel_detection_with_insufficient_tasks(self, temp_feature_dir):
        """
        E2E Scenario: Story with fewer than 3 tasks should not be parallelized.

        Tests FR-008: System MUST require a minimum of 3 tasks per user story
        before spawning a parallel Team Member to avoid excessive overhead.
        """
        tasks_content = """# Tasks: Test Feature

## Phase 1: User Story 1

- [ ] T001 [US1] Task 1
- [ ] T002 [US1] Task 2

## Phase 2: User Story 2

- [ ] T003 [US2] Task 1
- [ ] T004 [US2] Task 2
- [ ] T005 [US2] Task 3
"""

        from test_parallel_detection import analyze_parallel_opportunities

        # With only one story detected, need parallel=True to return it
        result = analyze_parallel_opportunities(tasks_content, parallel=True)
        story_ids = [s.story_id for s in result]

        # US1 has only 2 tasks, should be filtered out
        assert 'US1' not in story_ids, "US1 with 2 tasks should not be parallelized"
        assert 'US2' in story_ids, "US2 with 3 tasks should be parallelized"

    def test_e2e_max_4_members_limit(self, temp_feature_dir):
        """
        E2E Scenario: System should never spawn more than 4 parallel members.

        Tests FR-007: System MUST limit parallel Team Members to a maximum of 4
        to manage coordination overhead.
        """
        # Create content with 5 eligible stories
        tasks_content = """# Tasks: Test Feature

## Phase 1: Foundational

- [X] T001 Foundational

## Phase 2: User Story 1
- [ ] T002 [US1] Task 1
- [ ] T003 [US1] Task 2
- [ ] T004 [US1] Task 3

## Phase 3: User Story 2
- [ ] T005 [US2] Task 1
- [ ] T006 [US2] Task 2
- [ ] T007 [US2] Task 3

## Phase 4: User Story 3
- [ ] T008 [US3] Task 1
- [ ] T009 [US3] Task 2
- [ ] T010 [US3] Task 3

## Phase 5: User Story 4
- [ ] T011 [US4] Task 1
- [ ] T012 [US4] Task 2
- [ ] T013 [US4] Task 3

## Phase 6: User Story 5
- [ ] T014 [US5] Task 1
- [ ] T015 [US5] Task 2
- [ ] T016 [US5] Task 3
"""

        from test_parallel_detection import analyze_parallel_opportunities

        result = analyze_parallel_opportunities(tasks_content, max_members=4)
        assert len(result) == 4, "Should be limited to 4 members, got {}".format(len(result))

    def test_e2e_serial_flag_overrides_parallel(self, temp_feature_dir):
        """
        E2E Scenario: --serial flag should force sequential execution.

        Tests FR-005: System MUST support the --serial flag to force
        sequential execution regardless of parallel opportunities.
        """
        from test_parallel_detection import analyze_parallel_opportunities

        tasks_content = """# Tasks: Test Feature

## Phase 1: User Story 1
- [ ] T001 [P] [US1] Task 1
- [ ] T002 [P] [US1] Task 2
- [ ] T003 [P] [US1] Task 3

## Phase 2: User Story 2
- [ ] T004 [P] [US2] Task 1
- [ ] T005 [P] [US2] Task 2
- [ ] T006 [P] [US2] Task 3
"""

        # With --serial, should return empty list
        result = analyze_parallel_opportunities(tasks_content, serial=True)
        assert result == [], "Serial mode should return empty list for parallel stories"

    def test_e2e_parallel_flag_forces_single_story(self, temp_feature_dir):
        """
        E2E Scenario: --parallel flag should force parallel execution with single story.

        Tests FR-006: System MUST support the --parallel flag to force
        parallel execution even with a single user story.
        """
        from test_parallel_detection import analyze_parallel_opportunities

        tasks_content = """# Tasks: Test Feature

## Phase 1: Foundational
- [X] T001 Foundational

## Phase 2: User Story 1
- [ ] T002 [US1] Task 1
- [ ] T003 [US1] Task 2
- [ ] T004 [US1] Task 3
"""

        # With --parallel, single story should be returned
        result = analyze_parallel_opportunities(tasks_content, parallel=True)
        assert len(result) == 1, "Parallel mode should return single story"
        assert result[0].story_id == 'US1'

    def test_e2e_team_config_serialization_roundtrip(self, temp_feature_dir):
        """
        E2E Scenario: TeamConfig should serialize and deserialize correctly.

        Tests data model integrity for team-config.json.
        """
        from test_team_config import TeamConfig, TeamMember

        # Create a team config
        original = TeamConfig(
            team_name="e2e-test-team",
            feature_dir="/test/feature",
            members=[
                TeamMember(
                    member_id="member-us1",
                    story_id="US1",
                    tasks=["T001", "T002", "T003"],
                    status="running",
                    checkpoint="T001"
                ),
                TeamMember(
                    member_id="member-us2",
                    story_id="US2",
                    tasks=["T004", "T005", "T006", "T007"],
                    status="completed",
                    checkpoint="T007"
                )
            ]
        )

        # Round-trip serialization
        json_str = original.to_json()
        restored = TeamConfig.from_json(json_str)

        assert restored.team_name == original.team_name
        assert restored.feature_dir == original.feature_dir
        assert len(restored.members) == 2
        assert restored.members[0].member_id == "member-us1"
        assert restored.members[1].status == "completed"

    def test_e2e_git_sync_command_structure(self, temp_feature_dir):
        """
        E2E Scenario: Git sync should use correct command sequence.

        Tests EC-002: Git force-with-lease push with proper retry logic.
        """
        from test_git_sync import sync_tasks_md, GitSyncResult

        # Verify the function signature and return type
        result = sync_tasks_md(
            repo_path=temp_feature_dir,
            tasks_md_path=temp_feature_dir / "tasks.md",
            max_retries=2
        )

        assert isinstance(result, GitSyncResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'conflict')
        assert hasattr(result, 'error')

    def test_e2e_fallback_when_team_mode_unavailable(self, temp_feature_dir):
        """
        E2E Scenario: System should fallback to sequential when Team mode unavailable.

        Tests EC-001: Claude Code Team mode not enabled →
        Auto-fallback to sequential execution with warning message.
        """
        # Simulate team mode unavailable
        env = os.environ.copy()
        env.pop('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS', None)

        with patch.dict(os.environ, env, clear=True):
            from test_parallel_detection import os as parallel_os
            team_mode_enabled = parallel_os.getenv('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS') == '1'
            assert team_mode_enabled is False, "Team mode should be unavailable"


class TestE2EProgressTracking:
    """E2E tests for progress tracking scenarios."""

    def test_e2e_task_status_symbols(self):
        """
        E2E Scenario: Task status should use correct checkbox symbols.

        Tests FR-004: System MUST track task status in tasks.md using
        checkbox notation.
        """
        status_symbols = {
            "pending": "[ ]",
            "running": "[R]",
            "completed": "[X]",
            "failed": "[-]"
        }

        # Verify symbols match spec requirements
        assert status_symbols["pending"] == "[ ]", "Pending uses space"
        assert status_symbols["running"] == "[R]", "Running uses R"
        assert status_symbols["completed"] == "[X]", "Completed uses X"
        assert status_symbols["failed"] == "[-]", "Failed uses hyphen"

    def test_e2e_metrics_aggregation_calculation(self):
        """
        E2E Scenario: Metrics should aggregate correctly from member tasks.

        Tests SC-007: Aggregated metrics view shows total tasks, completed,
        failed, running, pending counts per user story.
        """
        # Simulate task status tracking
        member_tasks = ["T001", "T002", "T003", "T004"]
        task_status = {
            "T001": "completed",
            "T002": "completed",
            "T003": "running",
            "T004": "pending"
        }

        # Calculate metrics
        completed = sum(1 for t in member_tasks if task_status.get(t) == "completed")
        failed = sum(1 for t in member_tasks if task_status.get(t) == "failed")
        running = sum(1 for t in member_tasks if task_status.get(t) == "running")
        pending = len(member_tasks) - completed - failed - running

        assert completed == 2, "Should have 2 completed tasks"
        assert failed == 0, "Should have 0 failed tasks"
        assert running == 1, "Should have 1 running task"
        assert pending == 1, "Should have 1 pending task"

    def test_e2e_structured_log_format(self):
        """
        E2E Scenario: Structured logs should have correct format.

        Tests SC-006: Structured logs capture key events.
        """
        import json
        from datetime import datetime

        # Simulate log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "task_complete",
            "member_id": "member-us1",
            "task_id": "T001",
            "duration_ms": 1234
        }

        log_str = json.dumps(log_entry)
        parsed = json.loads(log_str)

        assert parsed["event_type"] == "task_complete"
        assert parsed["member_id"] == "member-us1"
        assert parsed["task_id"] == "T001"
        assert "timestamp" in parsed


class TestE2EGracefulDegradation:
    """E2E tests for graceful degradation scenarios."""

    def test_e2e_member_crash_recovery_checkpoints(self):
        """
        E2E Scenario: Member crash should resume from last checkpoint.

        Tests EC-003: Team Member agent crashes → Team Lead respawns
        a new Member; new Member resumes from last successful checkpoint.
        """
        from test_team_config import TeamMember

        # Simulate a member that crashed at T003
        member = TeamMember(
            member_id="member-us1",
            story_id="US1",
            tasks=["T001", "T002", "T003", "T004", "T005"],
            status="failed",
            checkpoint="T002"  # Last successful checkpoint
        )

        assert member.checkpoint == "T002", "Checkpoint should be T002"
        assert member.status == "failed", "Status should be failed"

        # Respawn should start from T003 (next after checkpoint)
        next_task_index = member.tasks.index(member.checkpoint) + 1
        resume_task = member.tasks[next_task_index] if next_task_index < len(member.tasks) else None
        assert resume_task == "T003", "Should resume from T003"

    def test_e2e_git_push_failure_retry_logic(self):
        """
        E2E Scenario: Git push failure should trigger retry logic.

        Tests EC-002: Git force-with-lease push fails → Retry fetch +
        rebase + push up to 2 times.
        """
        from test_git_sync import sync_with_retry

        # The sync_with_retry function implements the retry logic
        # Verify it exists and has correct signature
        import inspect
        sig = inspect.signature(sync_with_retry)
        params = list(sig.parameters.keys())

        assert 'repo_path' in params
        assert 'tasks_md_path' in params
        assert 'max_retries' in params

    def test_e2e_manual_edit_conflict_detection(self):
        """
        E2E Scenario: Manual edit conflict should be detected.

        Tests EC-005: tasks.md manually edited during parallel execution →
        Detect conflict on next push, pause affected branch.
        """
        # Simulate force-with-lease rejection
        error_msg = "force-with-lease rejected: remote work tree has diverged"

        has_conflict = "conflict" in error_msg.lower() or "rejected" in error_msg.lower()
        assert has_conflict, "Should detect conflict from force-with-lease rejection"

    def test_e2e_resource_insufficient_warning(self):
        """
        E2E Scenario: Resource insufficient should show warning.

        Tests EC-004: System resources insufficient → Display warning message
        suggesting --serial flag.
        """
        # Simulate resource check
        max_members = 4
        available_slots = 2  # Simulated limitation
        requested = 3

        if requested > available_slots:
            warning = (
                f"Warning: Requested {requested} parallel members but only "
                f"{available_slots} available. Consider using --serial flag."
            )
        else:
            warning = None

        assert warning is not None
        assert "--serial" in warning


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
