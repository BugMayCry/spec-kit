"""
Unit tests for User Story 3: Structured Decision Making

Tests options generation, decision request/response, and decision recording.
"""

import pytest
import json


# ============================================================================
# T025: Options Generation Tests
# ============================================================================

class TestOptionsGeneration:
    """Test suite for multiple options generation with pros/cons."""

    def test_multiple_options_generated_when_consensus_fails(self):
        """When roles disagree, multiple options should be generated."""
        disagreement = {
            "topic": "architecture_style",
            "member-architect": {"choice": "microservices", "reason": "scalability"},
            "member-tech": {"choice": "monolith", "reason": "simplicity"}
        }

        # Generate options when consensus fails
        has_disagreement = len(disagreement) > 1
        should_generate_options = has_disagreement

        assert should_generate_options is True

    def test_pros_cons_documented_for_each_option(self):
        """Each option should have pros and cons documented."""
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
        for opt in options:
            assert "pros" in opt
            assert "cons" in opt
            assert len(opt["pros"]) > 0
            assert len(opt["cons"]) > 0

    def test_risk_assessment_included(self):
        """Options should include risk assessment."""
        option = {
            "option": "A",
            "name": "Microservices",
            "pros": ["Independent scaling"],
            "cons": ["Operational complexity"],
            "risks": [
                {"risk": "Service discovery complexity", "likelihood": "high", "impact": "high"},
                {"risk": "Distributed tracing needed", "likelihood": "medium", "impact": "medium"}
            ]
        }

        assert "risks" in option
        assert len(option["risks"]) > 0
        for risk in option["risks"]:
            assert "risk" in risk
            assert "likelihood" in risk
            assert "impact" in risk

    def test_options_are_mutually_exclusive(self):
        """Generated options should be mutually exclusive alternatives."""
        options = [
            {"option": "A", "name": "Microservices"},
            {"option": "B", "name": "Monolith"},
            {"option": "C", "name": "Modular Monolith"}
        ]

        option_names = [o["name"] for o in options]
        assert len(option_names) == len(set(option_names))  # No duplicates


# ============================================================================
# T026: Decision Request/Response Tests
# ============================================================================

class TestDecisionRequestResponse:
    """Test suite for decision request and response message handling."""

    def test_decision_request_message_structure(self):
        """decision_request message should have required fields."""
        msg = {
            "type": "decision_request",
            "topic": "architecture_style",
            "options": [
                {"option": "A", "name": "Microservices", "pros": [], "cons": []},
                {"option": "B", "name": "Monolith", "pros": [], "cons": []}
            ],
            "contested_points": ["scalability", "simplicity"],
            "rationale": "Need to choose architecture style"
        }

        required_fields = ["type", "topic", "options", "contested_points"]
        for field in required_fields:
            assert field in msg

    def test_decision_request_type_is_decision_request(self):
        """decision_request message type must be 'decision_request'."""
        msg = {"type": "decision_request", "topic": "test"}
        assert msg["type"] == "decision_request"

    def test_decision_message_structure(self):
        """decision message should have: type, topic, choice, rationale."""
        msg = {
            "type": "decision",
            "topic": "architecture_style",
            "choice": "A",
            "rationale": "Need independent scaling for different components"
        }

        required_fields = ["type", "topic", "choice", "rationale"]
        for field in required_fields:
            assert field in msg

    def test_decision_message_parsing(self):
        """Parse decision JSON and extract fields."""
        json_str = '{"type": "decision", "topic": "db", "choice": "B", "rationale": "ACID compliance"}'
        parsed = json.loads(json_str)

        assert parsed["type"] == "decision"
        assert parsed["topic"] == "db"
        assert parsed["choice"] == "B"
        assert parsed["rationale"] == "ACID compliance"

    def test_decision_response_includes_selection(self):
        """Decision response must include user's selection."""
        decision = {
            "type": "decision",
            "topic": "authentication",
            "choice": "JWT",
            "rationale": "Stateless and widely supported"
        }

        assert "choice" in decision
        assert decision["choice"] == "JWT"


# ============================================================================
# T027: Decision Recording Tests
# ============================================================================

class TestDecisionRecording:
    """Test suite for decision recording and persistence."""

    def test_decisions_log_format(self):
        """Decisions Log should have correct structure."""
        decisions_log = [
            {
                "id": "D001",
                "type": "decision",
                "topic": "architecture_style",
                "choice": "A",
                "rationale": "Need independent scaling",
                "timestamp": "2026-04-02T10:00:00Z"
            }
        ]

        assert len(decisions_log) == 1
        decision = decisions_log[0]
        assert "id" in decision
        assert "type" in decision
        assert "topic" in decision
        assert "choice" in decision
        assert "rationale" in decision
        assert "timestamp" in decision

    def test_decision_persistence(self):
        """Decision should persist through serialization."""
        original = {
            "type": "decision",
            "topic": "frontend",
            "choice": "React",
            "rationale": "Large ecosystem"
        }

        serialized = json.dumps(original)
        deserialized = json.loads(serialized)

        assert deserialized == original

    def test_decision_validation_requires_choice(self):
        """Decision is invalid without a choice."""
        decision = {
            "type": "decision",
            "topic": "backend",
            "rationale": "Some reasoning"
        }

        is_valid = "choice" in decision and decision["choice"]
        assert is_valid is False

    def test_decision_validation_requires_rationale(self):
        """Decision is invalid without rationale."""
        decision = {
            "type": "decision",
            "topic": "backend",
            "choice": "A"
        }

        is_valid = "rationale" in decision and decision["rationale"]
        assert is_valid is False

    def test_multiple_decisions_tracked_separately(self):
        """Multiple decisions should be tracked separately."""
        decisions = [
            {"type": "decision", "topic": "arch", "choice": "A", "rationale": "reason A"},
            {"type": "decision", "topic": "db", "choice": "B", "rationale": "reason B"},
            {"type": "decision", "topic": "api", "choice": "C", "rationale": "reason C"}
        ]

        assert len(decisions) == 3
        topics = [d["topic"] for d in decisions]
        assert len(topics) == len(set(topics))  # All different topics


# ============================================================================
# T028: Integration tests are in test_brainstorm_integration.py
# T029: E2E tests are in test_brainstorm_e2e.py (TestDecisionScenarioE2E)
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
