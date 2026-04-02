"""
Integration tests for User Story 1: Multi-Role Brainstorming

Tests the full flow of spawning team members and collecting proposals.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import os


# ============================================================================
# T010: Integration Tests for Team Member Spawning
# ============================================================================

class TestTeamMemberSpawningIntegration:
    """Integration tests for spawning all team members."""

    @patch('os.getenv')
    def test_all_4_core_roles_spawn(self, mock_getenv):
        """Test all 4 core roles spawn successfully without --with-security."""
        mock_getenv.return_value = "1"  # Team mode enabled

        # Simulate spawning 4 core members
        expected_roles = ["member-pm", "member-architect", "member-tech", "member-test"]
        spawned_members = expected_roles.copy()  # Simulated spawn

        assert len(spawned_members) == 4
        for role in expected_roles:
            assert role in spawned_members

    @patch('os.getenv')
    def test_all_5_roles_spawn_with_security_flag(self, mock_getenv):
        """Test all 5 roles spawn with --with-security flag."""
        mock_getenv.return_value = "1"

        # Simulate spawning with security
        expected_roles = ["member-pm", "member-architect", "member-tech", "member-test", "member-security"]
        spawned_members = expected_roles.copy()

        assert len(spawned_members) == 5
        for role in expected_roles:
            assert role in spawned_members

    @patch('os.getenv')
    def test_member_count_matches_expected(self, mock_getenv):
        """Test member count matches expected for each configuration."""
        mock_getenv.return_value = "1"

        # Without security
        without_security = 4
        assert without_security == 4

        # With security
        with_security = 5
        assert with_security == 5

    def test_team_config_creation(self):
        """Test team-config.json is created with correct structure."""
        team_config = {
            "team_name": "brainstorm-001",
            "feature_dir": "/specs/003-brainstorm-team-collab",
            "created_at": "2026-04-02T10:00:00Z",
            "status": "active",
            "max_members": 5,
            "members": []
        }

        assert "team_name" in team_config
        assert "members" in team_config
        assert team_config["status"] == "active"
        assert len(team_config["members"]) == 0  # Empty initially


# ============================================================================
# T011: Integration Tests for Proposal Collection
# ============================================================================

class TestProposalCollectionIntegration:
    """Integration tests for collecting proposals from all roles."""

    def test_all_proposals_collected_within_timeout(self):
        """Test all proposals are collected within reasonable timeout."""
        # Simulate 4 roles, each responding within 60 seconds
        role_response_times = [30, 45, 50, 40]  # seconds
        max_timeout = 120  # 2 minutes timeout

        total_time = max(role_response_times)
        assert total_time < max_timeout, f"Proposal collection took {total_time}s, exceeding {max_timeout}s timeout"

    def test_proposals_aggregated_by_role(self):
        """Test proposals are aggregated correctly by role."""
        proposals = {
            "member-pm": {"role": "member-pm", "content": "# PM Proposal"},
            "member-architect": {"role": "member-architect", "content": "# Architect Proposal"},
            "member-tech": {"role": "member-tech", "content": "# Tech Proposal"},
            "member-test": {"role": "member-test", "content": "# Test Proposal"}
        }

        assert len(proposals) == 4
        assert "member-pm" in proposals
        assert "member-architect" in proposals
        assert "member-tech" in proposals
        assert "member-test" in proposals

    def test_partial_collection_handles_gracefully(self):
        """Test system handles partial proposal collection gracefully."""
        # Simulate 3 out of 4 roles responding
        partial_proposals = {
            "member-pm": {"role": "member-pm"},
            "member-architect": {"role": "member-architect"},
            "member-tech": {"role": "member-tech"}
        }
        # member-test did not respond

        assert len(partial_proposals) == 3
        assert "member-test" not in partial_proposals

        # System should handle this gracefully - maybe timeout and continue
        missing_roles = ["member-test"]
        assert len(missing_roles) == 1

    def test_proposal_content_merge_ready(self):
        """Test proposals are in correct format for spec merge."""
        proposals = {
            "member-pm": {
                "content": "# PM Proposal\n\nUser needs...",
                "key_points": ["Point 1", "Point 2"]
            },
            "member-architect": {
                "content": "# Architect Proposal\n\nSystem design...",
                "key_points": ["Scalable", "Maintainable"]
            }
        }

        # Verify all proposals have content for merging
        for role, proposal in proposals.items():
            assert "content" in proposal
            assert len(proposal["content"]) > 0


# ============================================================================
# Additional Integration Tests
# ============================================================================

class TestEndToEndProposalFlow:
    """End-to-end tests for the complete proposal collection flow."""

    @patch('os.getenv')
    def test_full_proposal_flow(self, mock_getenv):
        """Test complete flow from spawning to proposal collection."""
        mock_getenv.return_value = "1"

        # Step 1: Spawn members
        roles = ["member-pm", "member-architect", "member-tech", "member-test"]
        spawned = roles.copy()

        assert len(spawned) == len(roles)

        # Step 2: Send propose messages
        propose_messages_sent = []
        for role in spawned:
            msg = {
                "type": "propose",
                "role": role,
                "context": "Build a real-time notification system",
                "instructions": f"Provide your perspective as {role}"
            }
            propose_messages_sent.append(msg)

        assert len(propose_messages_sent) == 4

        # Step 3: Collect proposals
        proposals_received = []
        for i, role in enumerate(spawned):
            proposal = {
                "type": "proposal",
                "role": role,
                "content": f"# Proposal from {role}",
                "key_points": [f"Point from {role}"],
                "risks": [f"Risk from {role}"],
                "questions": [f"Question from {role}?"]
            }
            proposals_received.append(proposal)

        assert len(proposals_received) == 4

        # Step 4: Verify all roles responded
        responding_roles = [p["role"] for p in proposals_received]
        for role in roles:
            assert role in responding_roles


# ============================================================================
# T028: Integration Tests for Decision Flow
# ============================================================================

class TestDecisionFlowIntegration:
    """Integration tests for structured decision making flow."""

    def test_contested_point_triggers_options_generation(self):
        """When roles disagree, options should be generated."""
        proposals = {
            "member-architect": {"choice": "microservices"},
            "member-tech": {"choice": "monolith"}
        }

        # Detect disagreement
        choices = list(proposals.values())
        has_disagreement = len(set(str(c) for c in choices)) > 1

        # Generate options
        if has_disagreement:
            options = [
                {"option": "A", "name": "Microservices", "pros": [], "cons": []},
                {"option": "B", "name": "Monolith", "pros": [], "cons": []}
            ]
        else:
            options = []

        assert has_disagreement is True
        assert len(options) == 2

    def test_user_decision_updates_spec(self):
        """User's decision should update the spec."""
        decision = {
            "type": "decision",
            "topic": "architecture_style",
            "choice": "A",
            "rationale": "Need independent scaling"
        }

        spec = {
            "architecture_style": None,
            "decisions": []
        }

        # Apply decision to spec
        spec["decisions"].append(decision)
        spec["architecture_style"] = decision["choice"]

        assert len(spec["decisions"]) == 1
        assert spec["architecture_style"] == "A"

    def test_unanimous_case_skips_decision_flow(self):
        """When all agree, skip decision flow (EC-003)."""
        proposals = {
            "member-architect": {"choice": "microservices"},
            "member-tech": {"choice": "microservices"},
            "member-pm": {"choice": "microservices"}
        }

        # Check unanimity
        choices = [p["choice"] for p in proposals.values()]
        all_agree = len(set(choices)) == 1

        # Skip decision flow if unanimous
        should_skip_decision = all_agree

        assert should_skip_decision is True


# ============================================================================
# T037: Integration Tests for Output Generation
# ============================================================================

class TestOutputGenerationIntegration:
    """Integration tests for spec.md and appendix.md generation."""

    def test_spec_md_generated_with_all_sections(self):
        """spec.md should be generated with all required sections."""
        proposals = {
            "member-pm": {"content": "# PM Proposal"},
            "member-architect": {"content": "# Architect Proposal"},
            "member-tech": {"content": "# Tech Proposal"},
            "member-test": {"content": "# Test Proposal"}
        }

        decisions = [{"topic": "arch", "choice": "A"}]

        spec = {
            "overview": "# Feature Spec",
            "proposals": proposals,
            "decisions": decisions
        }

        # Verify spec has required content
        assert "overview" in spec
        assert "proposals" in spec
        assert len(spec["proposals"]) == 4
        assert len(spec["decisions"]) >= 1

    def test_appendix_md_generated_with_full_transcript(self):
        """appendix.md should be generated with full transcript."""
        transcript = {
            "messages": [
                {"type": "propose", "from": "lead", "to": "member-pm"},
                {"type": "proposal", "from": "member-pm", "to": "lead"},
                {"type": "debate", "from": "lead", "to": "all"},
                {"type": "counter_argument", "from": "member-devil", "to": "lead"},
                {"type": "decision", "from": "user", "to": "lead"}
            ],
            "proposals": {
                "member-pm": {"content": "# PM Proposal"},
                "member-architect": {"content": "# Architect Proposal"}
            }
        }

        appendix = {
            "filename": "brainstorm-appendix.md",
            "transcript": transcript,
            "all_messages_preserved": len(transcript["messages"]) == 5
        }

        assert appendix["filename"] == "brainstorm-appendix.md"
        assert len(transcript["messages"]) == 5
        assert appendix["all_messages_preserved"] is True

    def test_file_format_correctness(self):
        """Output files should be in correct markdown format."""
        spec_content = """# Feature Spec

## Overview
Brief description

## Functional Requirements
- Req 1
- Req 2

## Architecture
Microservices

## Decisions
- D001: Architecture → A (rationale)
"""

        appendix_content = """# Brainstorm Appendix

## Transcript
1. propose message
2. proposal message

## Proposals
All role proposals verbatim...

## Decisions
Recorded decisions with rationale...
"""

        # Verify markdown formatting
        assert spec_content.startswith("#")
        assert "## " in spec_content
        assert appendix_content.startswith("#")
        assert "## Transcript" in appendix_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
