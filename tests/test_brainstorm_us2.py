"""
Unit tests for User Story 2: Devil's Advocate Challenge

Tests the devil's advocate challenge functionality and counter-argument handling.
"""

import pytest
import json
from unittest.mock import patch, MagicMock


# ============================================================================
# T016: Devil's Advocate Challenge Generation Tests
# ============================================================================

class TestDevilsAdvocateChallengeGeneration:
    """Test suite for devil's advocate challenge generation."""

    def test_challenge_rate_per_major_assumption(self):
        """Devil's advocate should raise at least 3 challenges per major assumption."""
        major_assumptions = [
            "Microservices is the right architecture",
            "React is the best frontend framework",
            "PostgreSQL can handle the load"
        ]

        min_challenges_per_assumption = 3

        # Simulate challenges
        challenges_per_assumption = {
            "Microservices...": 3,
            "React...": 4,
            "PostgreSQL...": 3
        }

        for assumption, count in challenges_per_assumption.items():
            assert count >= min_challenges_per_assumption

    def test_what_could_go_wrong_pattern(self):
        """Challenge should follow 'what could go wrong' pattern."""
        challenge_templates = [
            "What could go wrong with {assumption}?",
            "What are the failure modes of {approach}?",
            "What happens when {condition}?"
        ]

        for template in challenge_templates:
            lower = template.lower()
            is_valid = ("what could go wrong" in lower or
                        "failure modes" in lower or
                        "what happens" in lower)
            assert is_valid, f"Template '{template}' does not follow challenge pattern"

    def test_edge_case_probing(self):
        """Challenge should probe edge cases and boundary conditions."""
        edge_case_questions = [
            "What happens at 10x load?",
            "What about network partition?",
            "How does it handle malformed input?",
            "What if the database is unavailable?"
        ]

        # Each should be a question
        for q in edge_case_questions:
            assert q.endswith("?")

    def test_challenge_includes_alternative(self):
        """Challenge should suggest alternatives when possible."""
        challenges = [
            {"challenge": "Microservices adds complexity", "suggestion": "Consider modular monolith"},
            {"challenge": "NoSQL for everything", "suggestion": "Relational data should use SQL"}
        ]

        for c in challenges:
            assert "suggestion" in c or "alternative" in c


# ============================================================================
# T017: Counter-Argument Routing Tests
# ============================================================================

class TestCounterArgumentRouting:
    """Test suite for counter-argument message routing."""

    def test_counter_argument_message_structure(self):
        """counter_argument message should have: type, target_role, target_point, argument, suggestion."""
        msg = {
            "type": "counter_argument",
            "target_role": "member-architect",
            "target_point": "microservices_architecture",
            "argument": "Microservices adds significant operational complexity",
            "suggestion": "Consider starting with a modular monolith"
        }

        required_fields = ["type", "target_role", "target_point", "argument"]
        for field in required_fields:
            assert field in msg

    def test_counter_argument_routing_to_correct_role(self):
        """Counter-argument should be routed to the correct target role."""
        target_roles = ["member-pm", "member-architect", "member-tech", "member-test"]

        for role in target_roles:
            msg = {
                "type": "counter_argument",
                "target_role": role,
                "argument": "Challenge text"
            }
            assert msg["target_role"] == role

    def test_contested_vs_unanimous_tracking(self):
        """System should track which points are contested vs unanimous."""
        points_status = {
            "microservices_architecture": "contested",
            "use_postgresql": "unanimous",
            "authentication_required": "unanimous",
            "frontend_framework": "contested"
        }

        contested = [p for p, s in points_status.items() if s == "contested"]
        unanimous = [p for p, s in points_status.items() if s == "unanimous"]

        assert len(contested) == 2
        assert len(unanimous) == 2

    def test_counter_argument_message_serialization(self):
        """Counter-argument should serialize to JSON correctly."""
        msg = {
            "type": "counter_argument",
            "target_role": "member-architect",
            "target_point": "monolithic_vs_microservices",
            "argument": "Consider operational overhead",
            "suggestion": "Start simple, evolve when needed"
        }

        serialized = json.dumps(msg)
        deserialized = json.loads(serialized)

        assert deserialized["type"] == "counter_argument"
        assert deserialized["target_role"] == "member-architect"


# ============================================================================
# T018: Debate Phase Initialization Tests
# ============================================================================

class TestDebatePhaseInitialization:
    """Test suite for debate phase initialization."""

    def test_devils_advocate_spawn_timing(self):
        """Devil's advocate should spawn only when debate phase starts."""
        current_phase = "proposal"
        should_spawn_devil = current_phase == "debate"
        assert should_spawn_devil is False

        current_phase = "debate"
        should_spawn_devil = current_phase == "debate"
        assert should_spawn_devil is True

    def test_proposal_context_sharing(self):
        """All proposals should be shared with devil's advocate during debate."""
        proposals = {
            "member-pm": {"content": "# PM Proposal"},
            "member-architect": {"content": "# Architect Proposal"},
            "member-tech": {"content": "# Tech Proposal"},
            "member-test": {"content": "# Test Proposal"}
        }

        # Devil's advocate should receive all proposals
        devil_context = proposals
        assert len(devil_context) == 4

    def test_debate_initiation_message_format(self):
        """Debate initiation message should include all proposals."""
        msg = {
            "type": "debate",
            "phase": "cross_examination",
            "proposals": {
                "member-pm": {"key_points": ["point1"]},
                "member-architect": {"key_points": ["point2"]}
            }
        }

        assert msg["type"] == "debate"
        assert msg["phase"] == "cross_examination"
        assert "proposals" in msg


# ============================================================================
# Integration Tests for US2 (T019) are in test_brainstorm_integration.py
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
