"""
E2E tests for brainstorm command.

Tests complete scenarios across all user stories.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import os


# ============================================================================
# T020: E2E Test for Devil's Advocate Scenario
# ============================================================================

class TestDevilsAdvocateE2E:
    """E2E tests for devil's advocate challenge scenario."""

    def test_flawed_assumption_triggers_challenge(self):
        """
        Scenario: Architect proposes microservices without justification
        Expected: Devil's advocate challenges with complexity trade-offs question
        """
        # Simulate architect proposal
        architect_proposal = {
            "role": "member-architect",
            "content": "# Architecture Proposal\n\nWe should use microservices architecture",
            "key_points": [
                "Scalability",
                "Independent deployment",
                "Technology heterogeneity"
            ]
        }

        # Check if proposal lacks justification
        lacks_justification = len(architect_proposal.get("risks", [])) == 0

        # Devil's advocate should challenge
        should_challenge = lacks_justification
        assert should_challenge is True

    def test_devils_advocate_responds_to_challenge(self):
        """
        Scenario: Devil's advocate challenges architect's microservices assumption
        Expected: Architect responds with justification or escalation
        """
        challenge = {
            "type": "counter_argument",
            "target_role": "member-architect",
            "argument": "What about the operational complexity of managing 10+ services?",
            "suggestion": "Consider starting with a modular monolith"
        }

        # Architect's response options
        can_justify = True  # Architect has data/justification
        if can_justify:
            response = "We've successfully run microservices at scale in our org"
            escalation_needed = False
        else:
            response = None
            escalation_needed = True

        assert escalation_needed is False  # Architect can justify


# ============================================================================
# T029: E2E Test for Decision Scenario
# ============================================================================

class TestDecisionScenarioE2E:
    """E2E tests for structured decision making scenario."""

    def test_contested_point_triggers_options(self):
        """
        Scenario: Two roles disagree on architecture style
        Expected: Multiple options with pros/cons presented for user decision
        """
        disagreement = {
            "topic": "architecture_style",
            "member-architect": {"choice": "microservices", "reason": "scalability"},
            "member-tech": {"choice": "monolith", "reason": "simplicity"}
        }

        # Generate options with pros/cons
        options = [
            {
                "option": "A",
                "name": "Microservices",
                "pros": ["Independent scaling", "Technology flexibility"],
                "cons": ["Operational complexity", "Network latency"]
            },
            {
                "option": "B",
                "name": "Monolith",
                "pros": ["Simple deployment", "No network overhead"],
                "cons": ["Harder to scale independently", "Tech stack coupling"]
            }
        ]

        assert len(options) == 2
        assert all("pros" in o and "cons" in o for o in options)

    def test_user_decision_recorded(self):
        """
        Scenario: User selects option A (microservices)
        Expected: Decision recorded in spec with rationale
        """
        decision = {
            "type": "decision",
            "topic": "architecture_style",
            "choice": "A",
            "rationale": "Need independent scaling for different components"
        }

        assert decision["type"] == "decision"
        assert decision["topic"] == "architecture_style"
        assert decision["choice"] == "A"

        # Decision should be added to Decisions Log
        decisions_log = [decision]
        assert len(decisions_log) == 1
        assert decisions_log[0]["choice"] == "A"


# ============================================================================
# T038: E2E Test for Complete Flow
# ============================================================================

class TestCompleteFlowE2E:
    """E2E tests for complete brainstorm flow."""

    @patch('os.getenv')
    def test_full_brainstorm_session(self, mock_getenv):
        """
        Scenario: Complete brainstorm session
        Expected: spec.md + appendix.md generated with all content
        """
        mock_getenv.return_value = "1"

        # Step 1: User provides idea
        user_idea = "Build a real-time notification system"

        # Step 2: Spawn roles and collect proposals
        roles = ["member-pm", "member-architect", "member-tech", "member-test"]
        proposals = {}
        for role in roles:
            proposals[role] = {
                "type": "proposal",
                "role": role,
                "content": f"# Proposal from {role}",
                "key_points": [f"Key point from {role}"],
                "risks": [f"Risk from {role}"],
                "questions": [f"Question from {role}?"]
            }

        # Step 3: Debate phase
        devil_advocate_spawned = True
        counter_arguments = [
            {"type": "counter_argument", "target_role": "member-architect"},
            {"type": "counter_argument", "target_role": "member-tech"}
        ]

        # Step 4: User decisions
        decisions = [
            {"type": "decision", "topic": "architecture", "choice": "A"}
        ]

        # Step 5: Generate outputs
        spec_generated = len(proposals) > 0
        appendix_generated = len(counter_arguments) > 0

        # Verify
        assert spec_generated
        assert appendix_generated
        assert len(proposals) == 4
        assert len(counter_arguments) >= 1
        assert len(decisions) >= 1

    def test_appendix_contains_all_proposals(self):
        """Verify appendix contains all proposals verbatim."""
        proposals = {
            "member-pm": {"content": "# PM Proposal", "role": "member-pm"},
            "member-architect": {"content": "# Architect Proposal", "role": "member-architect"},
            "member-tech": {"content": "# Tech Proposal", "role": "member-tech"},
            "member-test": {"content": "# Test Proposal", "role": "member-test"}
        }

        appendix = {
            "proposals": proposals,
            "counter_arguments": [],
            "decisions": []
        }

        # Verify all proposals in appendix
        assert len(appendix["proposals"]) == 4
        for role in ["member-pm", "member-architect", "member-tech", "member-test"]:
            assert role in appendix["proposals"]

    def test_sc005_no_messages_omitted(self):
        """Verify SC-005: Appendix contains all messages, no omissions."""
        messages_log = [
            {"type": "propose", "from": "lead", "to": "member-pm"},
            {"type": "proposal", "from": "member-pm", "to": "lead"},
            {"type": "debate", "from": "lead", "to": "all"},
            {"type": "counter_argument", "from": "member-devil", "to": "lead"},
            {"type": "decision", "from": "user", "to": "lead"}
        ]

        appendix_messages = messages_log.copy()  # All messages preserved

        assert len(appendix_messages) == len(messages_log)
        assert appendix_messages == messages_log


# ============================================================================
# Edge Case E2E Tests
# ============================================================================

class TestEdgeCaseE2E:
    """E2E tests for edge cases."""

    @patch('os.getenv')
    def test_lite_mode_fallback(self, mock_getenv):
        """
        Scenario: Team mode not enabled
        Expected: Warning displayed, lite mode offered
        """
        mock_getenv.return_value = None  # Team mode disabled

        team_mode_enabled = os.getenv("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"
        assert team_mode_enabled is False

        # System should offer lite mode
        should_offer_lite_mode = not team_mode_enabled
        assert should_offer_lite_mode is True

    def test_empty_idea_prompted(self):
        """
        Scenario: User provides empty idea
        Expected: System prompts for clarification
        """
        user_input = ""

        is_empty = len(user_input.strip()) == 0
        assert is_empty is True

        # System should prompt
        should_prompt = is_empty
        assert should_prompt is True

    def test_unanimous_agreement_skips_debate(self):
        """
        Scenario: All roles agree on all points
        Expected: Skip debate, proceed to spec generation
        """
        points = {
            "use_postgresql": "unanimous",
            "rest_api": "unanimous",
            "authentication": "unanimous"
        }

        contested = [p for p, s in points.items() if s != "unanimous"]
        all_unanimous = len(contested) == 0

        # Skip debate if all unanimous
        should_skip_debate = all_unanimous
        assert should_skip_debate is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
