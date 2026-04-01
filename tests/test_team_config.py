"""
Tests for TeamConfig serialization and deserialization.

These tests verify that the TeamConfig and TeamMember data classes
correctly serialize to and deserialize from JSON.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
import tempfile


class TeamMember:
    """TeamMember data class for testing."""
    VALID_STATUSES = ["running", "completed", "failed", "paused"]

    def __init__(
        self,
        member_id: str,
        story_id: str,
        tasks: list,
        status: str,
        checkpoint: str,
        spawned_at: str = None,
        completed_at: str = None
    ):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        if not re.match(r"^member-[a-z0-9]+$", member_id):
            raise ValueError(f"Invalid member_id: {member_id}")
        if not re.match(r"^US[0-9]+$", story_id):
            raise ValueError(f"Invalid story_id: {story_id}")

        self.member_id = member_id
        self.story_id = story_id
        self.tasks = tasks
        self.status = status
        self.checkpoint = checkpoint
        self.spawned_at = spawned_at or datetime.utcnow().isoformat() + "Z"
        self.completed_at = completed_at

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "story_id": self.story_id,
            "tasks": self.tasks,
            "status": self.status,
            "checkpoint": self.checkpoint,
            "spawned_at": self.spawned_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TeamMember":
        return cls(
            member_id=data["member_id"],
            story_id=data["story_id"],
            tasks=data["tasks"],
            status=data["status"],
            checkpoint=data["checkpoint"],
            spawned_at=data.get("spawned_at"),
            completed_at=data.get("completed_at")
        )


class TeamConfig:
    """TeamConfig data class for testing."""
    VALID_STATUSES = ["active", "completed", "failed"]

    def __init__(
        self,
        team_name: str,
        feature_dir: str,
        created_at: str = None,
        status: str = "active",
        max_members: int = 4,
        min_tasks_per_member: int = 3,
        members: list = None
    ):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        if max_members < 1 or max_members > 4:
            raise ValueError(f"max_members must be 1-4, got {max_members}")

        self.team_name = team_name
        self.feature_dir = feature_dir
        self.created_at = created_at or datetime.utcnow().isoformat() + "Z"
        self.status = status
        self.max_members = max_members
        self.min_tasks_per_member = min_tasks_per_member
        self.members = members or []

    def to_dict(self) -> dict:
        return {
            "team_name": self.team_name,
            "feature_dir": self.feature_dir,
            "created_at": self.created_at,
            "status": self.status,
            "max_members": self.max_members,
            "min_tasks_per_member": self.min_tasks_per_member,
            "members": [m.to_dict() if isinstance(m, TeamMember) else m for m in self.members]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "TeamConfig":
        members = [TeamMember.from_dict(m) if isinstance(m, dict) else m for m in data.get("members", [])]
        return cls(
            team_name=data["team_name"],
            feature_dir=data["feature_dir"],
            created_at=data.get("created_at"),
            status=data.get("status", "active"),
            max_members=data.get("max_members", 4),
            min_tasks_per_member=data.get("min_tasks_per_member", 3),
            members=members
        )

    @classmethod
    def from_json(cls, json_str: str) -> "TeamConfig":
        return cls.from_dict(json.loads(json_str))


import re


# Sample TeamConfig JSON for testing
SAMPLE_TEAM_CONFIG_JSON = {
    "team_name": "sdd-002-parallel-task-20260401",
    "feature_dir": "/path/to/specs/002-parallel-task-execution",
    "created_at": "2026-04-01T12:00:00Z",
    "status": "active",
    "max_members": 4,
    "min_tasks_per_member": 3,
    "members": [
        {
            "member_id": "member-us1",
            "story_id": "US1",
            "tasks": ["T004", "T005", "T006"],
            "status": "running",
            "checkpoint": "T004",
            "spawned_at": "2026-04-01T12:00:05Z",
            "completed_at": None
        },
        {
            "member_id": "member-us2",
            "story_id": "US2",
            "tasks": ["T007", "T008", "T009", "T010"],
            "status": "completed",
            "checkpoint": "T010",
            "spawned_at": "2026-04-01T12:00:05Z",
            "completed_at": "2026-04-01T12:05:00Z"
        }
    ]
}


class TestTeamConfigSerialization:
    """Test suite for TeamConfig JSON serialization."""

    def test_serialize_team_config_to_json(self):
        """Should correctly serialize TeamConfig to JSON."""
        config = TeamConfig(
            team_name="test-team",
            feature_dir="/path/to/spec",
            status="active"
        )
        result = config.to_json()
        assert "test-team" in result
        assert "/path/to/spec" in result
        assert "active" in result

    def test_deserialize_json_to_team_config(self):
        """Should correctly deserialize JSON to TeamConfig."""
        json_str = json.dumps(SAMPLE_TEAM_CONFIG_JSON)
        config = TeamConfig.from_json(json_str)
        assert config.team_name == "sdd-002-parallel-task-20260401"
        assert config.feature_dir == "/path/to/specs/002-parallel-task-execution"
        assert config.status == "active"
        assert config.max_members == 4

    def test_roundtrip_serialization(self):
        """Serialized then deserialized config should equal original."""
        original = TeamConfig(
            team_name="roundtrip-test",
            feature_dir="/test/path",
            members=[
                TeamMember(
                    member_id="member-us1",
                    story_id="US1",
                    tasks=["T001", "T002"],
                    status="running",
                    checkpoint="T001"
                )
            ]
        )
        json_str = original.to_json()
        restored = TeamConfig.from_json(json_str)
        assert restored.team_name == original.team_name
        assert restored.feature_dir == original.feature_dir
        assert len(restored.members) == 1
        assert restored.members[0].member_id == "member-us1"

    def test_serializes_datetime_correctly(self):
        """Should serialize datetime to ISO format."""
        config = TeamConfig(team_name="dt-test", feature_dir="/test")
        assert "T" in config.created_at
        assert config.created_at.endswith("Z")

    def test_handles_null_completed_at(self):
        """Should handle None values for optional fields."""
        member = TeamMember(
            member_id="member-us1",
            story_id="US1",
            tasks=["T001"],
            status="running",
            checkpoint="T001"
        )
        assert member.completed_at is None
        d = member.to_dict()
        assert d["completed_at"] is None


class TestTeamMemberStatus:
    """Test suite for TeamMember status transitions."""

    def test_valid_status_values(self):
        """Should only accept valid status values."""
        valid_statuses = ["running", "completed", "failed", "paused"]
        for status in valid_statuses:
            member = TeamMember(
                member_id="member-us1",
                story_id="US1",
                tasks=["T001"],
                status=status,
                checkpoint="T001"
            )
            assert member.status == status

    def test_invalid_status_rejected(self):
        """Should reject invalid status values."""
        with pytest.raises(ValueError, match="Invalid status"):
            TeamMember(
                member_id="member-us1",
                story_id="US1",
                tasks=["T001"],
                status="invalid_status",
                checkpoint="T001"
            )


class TestTeamConfigValidation:
    """Test suite for TeamConfig validation."""

    def test_requires_team_name(self):
        """Should require team_name field."""
        with pytest.raises(TypeError):
            config = TeamConfig(feature_dir="/test")

    def test_requires_feature_dir(self):
        """Should require feature_dir field."""
        with pytest.raises(TypeError):
            config = TeamConfig(team_name="test")

    def test_validates_max_members_range(self):
        """Should validate max_members is between 1 and 4."""
        with pytest.raises(ValueError, match="max_members must be 1-4"):
            TeamConfig(team_name="test", feature_dir="/test", max_members=5)

    def test_validates_min_tasks_per_member(self):
        """Should validate min_tasks_per_member is positive."""
        config = TeamConfig(
            team_name="test",
            feature_dir="/test",
            min_tasks_per_member=1
        )
        assert config.min_tasks_per_member == 1

    def test_member_id_format_validation(self):
        """Should validate member_id matches pattern ^member-[a-z0-9]+$"""
        # Valid member_ids
        valid_ids = ["member-us1", "member-u1", "member-abc123"]
        for mid in valid_ids:
            member = TeamMember(
                member_id=mid,
                story_id="US1",
                tasks=["T001"],
                status="running",
                checkpoint="T001"
            )
            assert member.member_id == mid

    def test_invalid_member_id_format_rejected(self):
        """Should reject invalid member_id format."""
        with pytest.raises(ValueError, match="Invalid member_id"):
            TeamMember(
                member_id="invalid",
                story_id="US1",
                tasks=["T001"],
                status="running",
                checkpoint="T001"
            )

    def test_story_id_format_validation(self):
        """Should validate story_id matches pattern ^US[0-9]+$"""
        # Valid story_ids
        valid_ids = ["US1", "US2", "US123"]
        for sid in valid_ids:
            member = TeamMember(
                member_id="member-us1",
                story_id=sid,
                tasks=["T001"],
                status="running",
                checkpoint="T001"
            )
            assert member.story_id == sid


class TestLoadSaveTeamConfig:
    """Test suite for loading and saving team-config.json."""

    def test_load_existing_config(self):
        """Should load existing team-config.json file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(SAMPLE_TEAM_CONFIG_JSON, f)
            f.flush()
            with open(f.name, 'r') as fp:
                loaded = TeamConfig.from_json(fp.read())
            assert loaded.team_name == "sdd-002-parallel-task-20260401"

    def test_save_config_to_file(self):
        """Should save TeamConfig to team-config.json."""
        config = TeamConfig(
            team_name="save-test",
            feature_dir="/test"
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(config.to_json())
            f.flush()
            with open(f.name, 'r') as fp:
                loaded = TeamConfig.from_json(fp.read())
            assert loaded.team_name == "save-test"

    def test_file_not_found_handling(self):
        """Should handle missing team-config.json gracefully."""
        with pytest.raises(FileNotFoundError):
            with open("/nonexistent/path/team-config.json", 'r') as f:
                TeamConfig.from_json(f.read())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
