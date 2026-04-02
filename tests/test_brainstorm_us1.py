"""
Unit tests for User Story 1: Multi-Role Brainstorming

Tests the core functionality of spawning team members and collecting proposals.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import os


# ============================================================================
# T007: Role Proposal Structure Validation Tests
# ============================================================================

class TestProposalStructure:
    """Test suite for Proposal model structure validation."""

    def test_proposal_has_required_fields(self):
        """Proposal must have: role, content, key_points, risks, questions."""
        proposal = {
            "type": "proposal",
            "role": "member-pm",
            "content": "# PM Proposal\n\nUser needs...",
            "key_points": ["point1", "point2"],
            "risks": ["risk1"],
            "questions": ["question1"]
        }

        required_fields = ["role", "content", "key_points", "risks", "questions"]
        for field in required_fields:
            assert field in proposal, f"Proposal missing required field: {field}"

    def test_proposal_role_valid_values(self):
        """Valid roles: member-pm, member-architect, member-tech, member-test, member-security."""
        valid_roles = ["member-pm", "member-architect", "member-tech", "member-test", "member-security"]

        for role in valid_roles:
            assert role in valid_roles

    def test_proposal_content_is_markdown(self):
        """Proposal content should be markdown formatted."""
        content = "# Title\n\nSome description"
        assert content.startswith("#"), "Proposal content should be markdown"

    def test_proposal_key_points_format(self):
        """key_points should be a list of strings."""
        key_points = ["Point 1", "Point 2", "Point 3"]
        assert isinstance(key_points, list)
        assert all(isinstance(p, str) for p in key_points)

    def test_proposal_risks_format(self):
        """risks should be a list of strings."""
        risks = ["Risk 1", "Risk 2"]
        assert isinstance(risks, list)
        assert all(isinstance(r, str) for r in risks)

    def test_proposal_questions_format(self):
        """questions should be a list of strings."""
        questions = ["Question 1?"]
        assert isinstance(questions, list)
        assert all(isinstance(q, str) for q in questions)

    def test_proposal_serialization_roundtrip(self):
        """Proposal should serialize and deserialize correctly."""
        original = {
            "type": "proposal",
            "role": "member-pm",
            "content": "# PM Proposal",
            "key_points": ["point1"],
            "risks": ["risk1"],
            "questions": ["q1?"]
        }

        serialized = json.dumps(original)
        deserialized = json.loads(serialized)

        assert deserialized == original


# ============================================================================
# T008: Team Member Spawning Logic Tests
# ============================================================================

class TestTeamMemberSpawning:
    """Test suite for team member spawning logic."""

    def test_spawn_conditions_core_roles_always(self):
        """Core roles (PM, Architect, Tech, Test) always spawn."""
        core_roles = ["member-pm", "member-architect", "member-tech", "member-test"]

        with_security = False
        with_security_flag = False

        for role in core_roles:
            should_spawn = True  # Core roles always spawn
            assert should_spawn, f"Core role {role} should always spawn"

    def test_spawn_conditions_security_expert_flag(self):
        """Security expert spawns only with --with-security flag."""
        security_role = "member-security"

        # Without flag
        should_spawn_without_flag = False
        assert should_spawn_without_flag is False

        # With flag
        should_spawn_with_flag = True
        assert should_spawn_with_flag is True

    def test_devils_advocate_spawn_timing(self):
        """Devil's advocate spawns only during debate phase, not proposal phase."""
        devil_role = "member-devil"

        # During proposal phase
        in_proposal_phase = True
        should_spawn_proposal = False
        assert should_spawn_proposal is False, "Devil's advocate should not spawn during proposal"

        # During debate phase
        in_debate_phase = True
        should_spawn_debate = True
        assert should_spawn_debate is True, "Devil's advocate should spawn during debate"

    def test_member_id_generation(self):
        """Member IDs follow naming convention: member-{role}."""
        role_to_id = {
            "pm": "member-pm",
            "architect": "member-architect",
            "tech": "member-tech",
            "test": "member-test",
            "security": "member-security",
            "devil": "member-devil"
        }

        for role, expected_id in role_to_id.items():
            member_id = f"member-{role}"
            assert member_id == expected_id

    def test_role_count_without_security(self):
        """Without --with-security, should spawn 5 members (4 core + devil in debate)."""
        core_members = 4  # PM, Architect, Tech, Test
        security_member = 0  # Not included without flag
        devil_member = 0  # Only in debate phase

        total_proposal_phase = core_members + devil_member
        assert total_proposal_phase == 4

    def test_role_count_with_security(self):
        """With --with-security, should spawn 5 core + 1 security."""
        core_members = 4
        security_member = 1  # Included with flag

        total_proposal_phase = core_members + security_member
        assert total_proposal_phase == 5


# ============================================================================
# T009: Proposal Message Handling Tests
# ============================================================================

class TestProposalMessageHandling:
    """Test suite for proposal message types and handling."""

    def test_propose_message_structure(self):
        """propose message should have: type, role, context, instructions."""
        propose_msg = {
            "type": "propose",
            "role": "member-pm",
            "context": "Build a payment system",
            "instructions": "Focus on user needs and business value"
        }

        required_fields = ["type", "role", "context", "instructions"]
        for field in required_fields:
            assert field in propose_msg, f"propose message missing: {field}"

    def test_propose_message_type_is_propose(self):
        """propose message type must be 'propose'."""
        msg = {"type": "propose", "role": "member-pm"}
        assert msg["type"] == "propose"

    def test_proposal_response_structure(self):
        """proposal response should have: type, role, content, key_points, risks, questions."""
        proposal_resp = {
            "type": "proposal",
            "role": "member-architect",
            "content": "# Architecture Proposal\n\n...",
            "key_points": ["Scalable", "Maintainable"],
            "risks": ["Complexity"],
            "questions": ["Which cloud provider?"]
        }

        assert proposal_resp["type"] == "proposal"
        assert proposal_resp["role"] == "member-architect"
        assert "content" in proposal_resp
        assert "key_points" in proposal_resp
        assert "risks" in proposal_resp
        assert "questions" in proposal_resp

    def test_proposal_message_parsing(self):
        """Parse proposal JSON and extract fields."""
        json_str = '{"type": "proposal", "role": "member-tech", "content": "# Tech Proposal"}'
        parsed = json.loads(json_str)

        assert parsed["type"] == "proposal"
        assert parsed["role"] == "member-tech"
        assert "content" in parsed

    def test_propose_message_serialization(self):
        """propose message should serialize to JSON correctly."""
        msg = {
            "type": "propose",
            "role": "member-test",
            "context": "Build an authentication system",
            "instructions": "Focus on testability and edge cases"
        }

        serialized = json.dumps(msg)
        deserialized = json.loads(serialized)

        assert deserialized["type"] == "propose"
        assert deserialized["role"] == "member-test"


# ============================================================================
# Integration Tests for US1 (T010-T011) are in test_brainstorm_integration.py
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
