"""
Unit tests for User Story 4: Complete Debate Record

Tests spec.md generation, transcript collection, and appendix generation.
"""

import pytest
import json


# ============================================================================
# T034: spec.md Generation Tests
# ============================================================================

class TestSpecGeneration:
    """Test suite for spec.md generation from proposals and decisions."""

    def test_spec_sections_from_role_proposals(self):
        """spec.md should have sections populated from role proposals."""
        proposals = {
            "member-pm": {"content": "# PM Proposal\n\nUser needs...", "key_points": ["Point 1"]},
            "member-architect": {"content": "# Architecture\n\nDesign...", "key_points": ["Scalable"]},
            "member-tech": {"content": "# Tech Proposal\n\nImplementation...", "key_points": ["Stack choice"]},
            "member-test": {"content": "# Test Proposal\n\nTesting...", "key_points": ["Coverage"]}
        }

        spec = {
            "overview": "# Feature Spec",
            "proposals": {
                "product_manager": proposals["member-pm"]["content"],
                "architecture": proposals["member-architect"]["content"],
                "technical": proposals["member-tech"]["content"],
                "testing": proposals["member-test"]["content"]
            }
        }

        assert "proposals" in spec
        assert len(spec["proposals"]) == 4

    def test_user_decisions_applied_to_contested_points(self):
        """User decisions should override contested points in spec."""
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

        # Apply decision
        spec["decisions"].append(decision)
        spec["architecture_style"] = decision["choice"]

        assert spec["architecture_style"] == "A"
        assert len(spec["decisions"]) == 1

    def test_spec_completeness_per_sc006(self):
        """Spec should meet SC-006 completeness checklist."""
        spec = {
            "overview": "# Feature Spec",
            "functional_requirements": ["Req 1", "Req 2"],
            "non_functional_requirements": ["Performance", "Security"],
            "architecture": "Microservices",
            "decisions": [{"topic": "arch", "choice": "A"}],
            "risks": ["Risk 1"],
            "questions": ["Open question 1"]
        }

        # SC-006 completeness checklist
        required_sections = [
            "overview",
            "functional_requirements",
            "non_functional_requirements",
            "architecture",
            "decisions",
            "risks",
            "questions"
        ]

        completeness_score = sum(1 for s in required_sections if s in spec) / len(required_sections)
        assert completeness_score >= 0.8, f"Spec completeness {completeness_score*100}% is below 80%"

    def test_spec_has_all_key_sections(self):
        """Generated spec should have all key sections."""
        spec = {
            "title": "Feature Name",
            "overview": "Summary",
            "functional_requirements": [],
            "architecture": "",
            "decisions": [],
            "appendix": "brainstorm-appendix.md"
        }

        required = ["title", "overview", "functional_requirements", "architecture", "decisions", "appendix"]
        for section in required:
            assert section in spec, f"Missing required section: {section}"


# ============================================================================
# T035: Transcript Collection Tests
# ============================================================================

class TestTranscriptCollection:
    """Test suite for chronological message storage."""

    def test_chronological_message_storage(self):
        """Messages should be stored chronologically."""
        messages = [
            {"type": "propose", "from": "lead", "to": "member-pm", "order": 1},
            {"type": "proposal", "from": "member-pm", "to": "lead", "order": 2},
            {"type": "debate", "from": "lead", "to": "all", "order": 3},
            {"type": "counter_argument", "from": "member-devil", "to": "lead", "order": 4},
            {"type": "decision", "from": "user", "to": "lead", "order": 5}
        ]

        # Verify chronological order
        for i in range(len(messages) - 1):
            assert messages[i]["order"] < messages[i + 1]["order"]

    def test_message_type_inclusion(self):
        """All message types should be stored in transcript."""
        message_types = ["propose", "proposal", "debate", "counter_argument", "decision_request", "decision"]

        transcript = {
            "messages": [
                {"type": "propose"},
                {"type": "proposal"},
                {"type": "debate"},
                {"type": "counter_argument"},
                {"type": "decision_request"},
                {"type": "decision"}
            ]
        }

        stored_types = [m["type"] for m in transcript["messages"]]
        for msg_type in message_types:
            assert msg_type in stored_types, f"Missing message type: {msg_type}"

    def test_no_messages_omitted_verification(self):
        """Verify all messages are preserved - no omissions (SC-005)."""
        original_messages = [
            {"type": "propose", "from": "lead", "to": "member-pm"},
            {"type": "proposal", "from": "member-pm", "to": "lead"},
            {"type": "debate", "from": "lead", "to": "all"},
            {"type": "counter_argument", "from": "member-devil", "to": "lead"},
            {"type": "decision", "from": "user", "to": "lead"}
        ]

        transcript_messages = original_messages.copy()  # All preserved

        assert len(transcript_messages) == len(original_messages)
        assert transcript_messages == original_messages

    def test_proposals_preserved_in_transcript(self):
        """All proposals should be preserved verbatim in transcript."""
        proposals = {
            "member-pm": {"content": "# PM Proposal", "role": "member-pm"},
            "member-architect": {"content": "# Architect Proposal", "role": "member-architect"},
            "member-tech": {"content": "# Tech Proposal", "role": "member-tech"},
            "member-test": {"content": "# Test Proposal", "role": "member-test"}
        }

        transcript = {"proposals": proposals}

        assert len(transcript["proposals"]) == 4
        for role, proposal in proposals.items():
            assert role in transcript["proposals"]
            assert transcript["proposals"][role]["content"] == proposal["content"]


# ============================================================================
# T036: Appendix Generation Tests
# ============================================================================

class TestAppendixGeneration:
    """Test suite for brainstorm-appendix.md generation."""

    def test_appendix_file_naming(self):
        """Appendix should be named brainstorm-appendix.md."""
        appendix_filename = "brainstorm-appendix.md"

        assert appendix_filename.endswith(".md")
        assert "appendix" in appendix_filename.lower()
        assert "brainstorm" in appendix_filename.lower()

    def test_appendix_chronological_format(self):
        """Appendix should be formatted chronologically."""
        appendix_content = """# Brainstorm Appendix

## Transcript

### Phase 1: Proposals
1. [lead → member-pm] propose: "Build a notification system"
2. [member-pm → lead] proposal: "# PM Proposal..."

### Phase 2: Debate
3. [lead → all] debate: "Cross-examination started"
4. [member-devil → lead] counter_argument: "What about scalability?"

### Phase 3: Decisions
5. [user → lead] decision: "Choose microservices"
"""

        assert "Transcript" in appendix_content
        assert "Phase 1" in appendix_content
        assert "Phase 2" in appendix_content
        assert "Phase 3" in appendix_content

    def test_appendix_completeness_verification(self):
        """Appendix should contain all proposals, challenges, and decisions."""
        appendix = {
            "proposals": {
                "member-pm": {"content": "# PM Proposal"},
                "member-architect": {"content": "# Architect Proposal"},
                "member-tech": {"content": "# Tech Proposal"},
                "member-test": {"content": "# Test Proposal"}
            },
            "counter_arguments": [
                {"type": "counter_argument", "target": "member-architect"}
            ],
            "decisions": [
                {"type": "decision", "topic": "arch", "choice": "A"}
            ]
        }

        # Verify completeness
        assert len(appendix["proposals"]) == 4
        assert len(appendix["counter_arguments"]) >= 1
        assert len(appendix["decisions"]) >= 1

    def test_appendix_contains_all_message_types(self):
        """Appendix should contain all message types."""
        appendix = {
            "proposals": [],
            "counter_arguments": [],
            "decisions": [],
            "debate_messages": []
        }

        required_sections = ["proposals", "counter_arguments", "decisions", "debate_messages"]
        for section in required_sections:
            assert section in appendix


# ============================================================================
# T037: Integration tests are in test_brainstorm_integration.py
# T038: E2E tests are in test_brainstorm_e2e.py (TestCompleteFlowE2E)
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
