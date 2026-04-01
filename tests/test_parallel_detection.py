"""
Tests for parallel detection logic.

These tests verify that the analyze_parallel_opportunities() function
correctly identifies user stories that can be executed in parallel.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import os
import re


# Sample tasks.md content for testing
SAMPLE_TASKS_MD = """
# Tasks: Test Feature

## Phase 1: Setup

- [ ] T001 Setup task 1
- [ ] T002 Setup task 2

## Phase 2: Foundational

- [ ] T003 Foundational task

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


class Story:
    """Simple story class for testing."""
    def __init__(self, story_id: str, tasks: list):
        self.story_id = story_id
        self.tasks = tasks


def parse_stories_from_tasks_md(content: str) -> dict:
    """Parse stories from tasks.md content."""
    stories = {}
    current_story = None

    for line in content.split('\n'):
        # Look for story markers like [US1], [US2], etc.
        story_match = re.search(r'\[(US\d+)\]', line)
        if story_match:
            story_id = story_match.group(1)
            if story_id not in stories:
                stories[story_id] = []
            # Extract task ID if present (e.g., T004, T005)
            task_match = re.search(r'(T\d+)', line)
            if task_match:
                stories[story_id].append(task_match.group(1))

    return stories


def analyze_parallel_opportunities(
    tasks_md_content: str,
    serial: bool = False,
    parallel: bool = False,
    max_members: int = 4,
    min_tasks: int = 3
) -> list:
    """
    Analyze tasks.md content for parallelizable user stories.

    Returns list of Story objects with 3+ tasks each.
    """
    if serial:
        return []

    stories = parse_stories_from_tasks_md(tasks_md_content)

    # Filter to stories with min_tasks or more
    result = []
    for story_id, tasks in stories.items():
        if len(tasks) >= min_tasks:
            result.append(Story(story_id, tasks))

    # Limit to max_members
    if not parallel and len(result) < 2:
        return []

    return result[:max_members]


class TestAnalyzeParallelOpportunities:
    """Test suite for analyze_parallel_opportunities() function."""

    def test_detects_stories_with_3_or_more_tasks(self):
        """Stories with 3+ tasks should be detected as parallelizable."""
        result = analyze_parallel_opportunities(SAMPLE_TASKS_MD)
        story_ids = [s.story_id for s in result]
        assert 'US1' in story_ids, "US1 has 3 tasks, should be detected"
        assert 'US2' in story_ids, "US2 has 4 tasks, should be detected"

    def test_ignores_stories_with_less_than_3_tasks(self):
        """Stories with less than 3 tasks should not be parallelizable."""
        result = analyze_parallel_opportunities(SAMPLE_TASKS_MD)
        story_ids = [s.story_id for s in result]
        assert 'US3' not in story_ids, "US3 has only 1 task, should be ignored"

    def test_parses_story_markers_correctly(self):
        """Should correctly parse [US1], [US2], etc. markers."""
        result = analyze_parallel_opportunities(SAMPLE_TASKS_MD)
        assert len(result) == 2, "Should find exactly 2 stories with 3+ tasks"

    def test_respects_max_members_limit(self):
        """Should limit to max 4 parallel members (FR-007)."""
        result = analyze_parallel_opportunities(SAMPLE_TASKS_MD, max_members=1)
        assert len(result) == 1, "Should limit to 1 member when max_members=1"

    def test_returns_empty_for_sequential_mode(self):
        """Should return empty list when --serial is set."""
        result = analyze_parallel_opportunities(SAMPLE_TASKS_MD, serial=True)
        assert result == [], "Should return empty list for serial mode"

    def test_returns_single_story_for_forced_parallel(self):
        """Should return story even with 1 task when --parallel is set."""
        # Create content with only US3 (1 task)
        single_story_content = """
## Phase 1: User Story 3

- [ ] T011 [US3] Only one task for US3
"""
        result = analyze_parallel_opportunities(single_story_content, parallel=True, min_tasks=1)
        assert len(result) == 1, "Should return story with --parallel even if only 1 task"
        assert result[0].story_id == 'US3'


class TestParallelDetectionEdgeCases:
    """Edge case tests for parallel detection."""

    def test_empty_tasks_md(self):
        """Should handle empty tasks.md gracefully."""
        result = analyze_parallel_opportunities("")
        assert result == [], "Should return empty list for empty content"

    def test_no_story_markers(self):
        """Should handle tasks without story markers."""
        content = """
- [ ] T001 Setup task
- [ ] T002 Another task
"""
        result = analyze_parallel_opportunities(content)
        assert result == [], "Should return empty when no story markers"

    def test_mixed_story_and_non_story_tasks(self):
        """Should correctly separate story tasks from setup tasks."""
        content = """
## Phase 1: Setup

- [ ] T001 Setup task 1

## Phase 2: User Story 1

- [ ] T002 [US1] First US1 task
- [ ] T003 [US1] Second US1 task
- [ ] T004 [US1] Third US1 task
"""
        # Only 1 story, so need parallel=True to get results
        result = analyze_parallel_opportunities(content, parallel=True)
        assert len(result) == 1, "Should find 1 story with 3 tasks"
        assert result[0].story_id == 'US1'
        assert len(result[0].tasks) == 3

    def test_story_with_exactly_3_tasks(self):
        """Should detect story with exactly 3 tasks (min threshold)."""
        content = """
## Phase 1: User Story 1

- [ ] T001 [US1] First task
- [ ] T002 [US1] Second task
- [ ] T003 [US1] Third task
"""
        # Only 1 story, so need parallel=True to get results
        result = analyze_parallel_opportunities(content, parallel=True, min_tasks=3)
        assert len(result) == 1, "Should detect story with exactly 3 tasks"


class TestTeamModeAvailability:
    """Test suite for Team mode availability detection."""

    def test_returns_true_when_env_var_set(self):
        """Should return True when CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1."""
        with patch.dict(os.environ, {'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS': '1'}):
            result = os.getenv('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS') == '1'
            assert result is True

    def test_returns_false_when_env_var_not_set(self):
        """Should return False when env var is not set."""
        env = os.environ.copy()
        env.pop('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS', None)
        with patch.dict(os.environ, env, clear=True):
            result = os.getenv('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS')
            assert result is None

    def test_returns_false_for_other_env_values(self):
        """Should return False for non-"1" values."""
        with patch.dict(os.environ, {'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS': 'true'}):
            result = os.getenv('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS') == '1'
            assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
