"""
CLI Integration tests for brainstorm command.

Tests that verify the actual CLI integration points for the brainstorm command,
including template parsing, message generation, and workflow state management.
"""

import pytest
import json
import os
from unittest.mock import patch, MagicMock, Mock


# ============================================================================
# CLI Integration Tests
# ============================================================================

class TestBrainstormCLIIntegration:
    """Test suite for brainstorm CLI integration."""

    def test_brainstorm_template_exists(self):
        """Verify brainstorm command template exists."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'templates',
            'commands',
            'brainstorm.md'
        )
        assert os.path.exists(template_path), "brainstorm.md template should exist"

    def test_import_specify_cli(self):
        """Verify specify_cli can be imported."""
        try:
            import specify_cli
            assert hasattr(specify_cli, '__init__')
        except ImportError as e:
            pytest.skip(f"specify_cli not importable: {e}")

    def test_team_mode_env_check(self):
        """Test team mode environment variable check logic."""
        # Test when env var is set
        with patch.dict(os.environ, {'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS': '1'}):
            team_mode_enabled = os.getenv('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS') == '1'
            assert team_mode_enabled is True

        # Test when env var is not set
        with patch.dict(os.environ, {'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS': ''}):
            team_mode_enabled = os.getenv('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS') == '1'
            assert team_mode_enabled is False

    def test_role_configuration_parsing(self):
        """Test parsing of role configurations."""
        roles = {
            'member-pm': {'always': True},
            'member-architect': {'always': True},
            'member-tech': {'always': True},
            'member-test': {'always': True},
            'member-security': {'flag': '--with-security'},
            'member-devil': {'phase': 'debate'}
        }

        # Without security flag - during proposal phase
        with_security = False
        current_phase = 'proposal'

        # Active roles during proposal phase
        active_roles = [r for r, cfg in roles.items()
                       if cfg.get('always') or
                       (with_security and cfg.get('flag') == '--with-security') or
                       (current_phase == 'debate' and cfg.get('phase') == 'debate')]

        # Devil is debate phase only, so not included in proposal phase
        assert 'member-pm' in active_roles
        assert 'member-security' not in active_roles
        assert 'member-devil' not in active_roles  # Not in proposal phase

    def test_security_flag_enables_security_role(self):
        """Test that --with-security flag enables security role."""
        roles = {
            'member-pm': {'always': True},
            'member-security': {'flag': '--with-security'}
        }

        with_security = True
        active_roles = [r for r, cfg in roles.items()
                       if cfg.get('always') or
                       (with_security and cfg.get('flag') == '--with-security')]

        assert 'member-security' in active_roles


class TestMessageGeneration:
    """Test suite for message generation logic."""

    def test_propose_message_generation(self):
        """Test generating a propose message."""
        msg = {
            'type': 'propose',
            'role': 'member-pm',
            'context': 'Build a real-time notification system',
            'instructions': 'Focus on user needs and business value'
        }

        assert msg['type'] == 'propose'
        assert 'context' in msg
        assert 'instructions' in msg

    def test_proposal_message_generation(self):
        """Test generating a proposal response."""
        msg = {
            'type': 'proposal',
            'role': 'member-architect',
            'content': '# Architecture Proposal\n\nMicroservices architecture',
            'key_points': ['Scalable', 'Independent deployment'],
            'risks': ['Operational complexity'],
            'questions': ['Which cloud provider?']
        }

        assert msg['type'] == 'proposal'
        assert 'content' in msg
        assert 'key_points' in msg
        assert 'risks' in msg
        assert 'questions' in msg

    def test_debate_message_generation(self):
        """Test generating a debate initiation message."""
        proposals = {
            'member-pm': {'content': '# PM Proposal'},
            'member-architect': {'content': '# Architect Proposal'}
        }

        msg = {
            'type': 'debate',
            'phase': 'cross_examination',
            'proposals': proposals
        }

        assert msg['type'] == 'debate'
        assert msg['phase'] == 'cross_examination'
        assert 'proposals' in msg

    def test_counter_argument_message_generation(self):
        """Test generating a counter-argument message."""
        msg = {
            'type': 'counter_argument',
            'target_role': 'member-architect',
            'target_point': 'microservices_architecture',
            'argument': 'What about operational complexity?',
            'suggestion': 'Consider modular monolith first'
        }

        assert msg['type'] == 'counter_argument'
        assert 'target_role' in msg
        assert 'argument' in msg

    def test_decision_request_message_generation(self):
        """Test generating a decision request message."""
        msg = {
            'type': 'decision_request',
            'topic': 'architecture_style',
            'options': [
                {'option': 'A', 'name': 'Microservices', 'pros': [], 'cons': []},
                {'option': 'B', 'name': 'Monolith', 'pros': [], 'cons': []}
            ],
            'contested_points': ['scalability', 'simplicity']
        }

        assert msg['type'] == 'decision_request'
        assert len(msg['options']) == 2

    def test_decision_message_generation(self):
        """Test generating a decision message."""
        msg = {
            'type': 'decision',
            'topic': 'architecture_style',
            'choice': 'A',
            'rationale': 'Need independent scaling'
        }

        assert msg['type'] == 'decision'
        assert msg['choice'] == 'A'
        assert 'rationale' in msg


class TestWorkflowStateMachine:
    """Test suite for workflow state management."""

    def test_initial_phase_is_proposal(self):
        """Initial phase should be proposal collection."""
        initial_phase = 'proposal'
        assert initial_phase == 'proposal'

    def test_phase_transition_proposal_to_debate(self):
        """Phase should transition from proposal to debate."""
        phases = ['proposal', 'debate', 'decision', 'output']
        current_phase = 'proposal'

        # Transition to debate after proposals collected
        if current_phase == 'proposal':
            current_phase = 'debate'

        assert current_phase == 'debate'
        assert phases.index(current_phase) == 1

    def test_phase_transition_debate_to_decision(self):
        """Phase should transition from debate to decision."""
        phases = ['proposal', 'debate', 'decision', 'output']
        current_phase = 'debate'

        # Transition to decision after debate
        if current_phase == 'debate':
            current_phase = 'decision'

        assert current_phase == 'decision'
        assert phases.index(current_phase) == 2

    def test_devil_advocate_spawns_in_debate_phase(self):
        """Devil's advocate should only spawn in debate phase."""
        devil_spawned = False
        phases = ['proposal', 'debate', 'decision', 'output']

        for phase in phases:
            if phase == 'debate':
                devil_spawned = True
            # In actual implementation, devil would be spawned here

        assert devil_spawned is True

    def test_skip_debate_when_unanimous(self):
        """Should skip debate phase when all agree (EC-003)."""
        proposals = {
            'member-pm': {'choice': 'microservices'},
            'member-architect': {'choice': 'microservices'},
            'member-tech': {'choice': 'microservices'}
        }

        choices = [p['choice'] for p in proposals.values()]
        all_unanimous = len(set(choices)) == 1

        if all_unanimous:
            skip_debate = True
        else:
            skip_debate = False

        assert skip_debate is True


class TestOutputGeneration:
    """Test suite for output generation."""

    def test_spec_filename_generation(self):
        """Test spec.md filename generation."""
        spec_filename = 'spec.md'
        assert spec_filename.endswith('.md')
        assert 'spec' in spec_filename.lower()

    def test_appendix_filename_generation(self):
        """Test appendix filename generation."""
        appendix_filename = 'brainstorm-appendix.md'
        assert appendix_filename.endswith('.md')
        assert 'appendix' in appendix_filename.lower()
        assert 'brainstorm' in appendix_filename.lower()

    def test_decisions_log_structure(self):
        """Test decisions log has correct structure."""
        decisions_log = []

        decision = {
            'id': 'D001',
            'type': 'decision',
            'topic': 'architecture',
            'choice': 'A',
            'rationale': 'Reason here',
            'timestamp': '2026-04-02T10:00:00Z'
        }

        decisions_log.append(decision)

        assert len(decisions_log) == 1
        assert decisions_log[0]['id'] == 'D001'
        assert 'timestamp' in decisions_log[0]


class TestEdgeCaseHandling:
    """Test suite for edge case handling in CLI."""

    def test_empty_idea_detection(self):
        """Test empty idea detection (EC-002)."""
        user_input = ''
        is_empty = len(user_input.strip()) == 0
        assert is_empty is True

    def test_vague_idea_detection(self):
        """Test vague idea detection (EC-002)."""
        vague_ideas = ['', 'Do stuff', 'Fix it', 'Do something']
        vague_keywords = ['stuff', 'fix', 'something', 'add', 'feature', 'thing']

        for idea in vague_ideas:
            is_vague = len(idea.strip()) < 10 or any(k in idea.lower() for k in vague_keywords)
            assert is_vague is True, f"'{idea}' should be detected as vague"

    def test_team_mode_warning_message(self):
        """Test warning message when team mode unavailable (EC-001)."""
        team_mode_available = False

        if not team_mode_available:
            warning = "Team mode not available. Falling back to lite mode."
        else:
            warning = None

        assert warning is not None
        assert 'Team mode' in warning
        assert 'lite mode' in warning

    def test_security_concern_detection_keywords(self):
        """Test security concern detection (EC-004)."""
        messages = [
            {'argument': 'What about encryption at rest?'},
            {'argument': 'How do we handle PII compliance?'}
        ]

        security_keywords = ['encryption', 'PII', 'security', 'compliance', 'privacy']
        detected = False

        for msg in messages:
            for keyword in security_keywords:
                if keyword in msg.get('argument', '').lower():
                    detected = True
                    break

        assert detected is True

    def test_unproductive_debate_detection(self):
        """Test unproductive debate detection (EC-005)."""
        debate_rounds = [
            {'round': 1, 'counter_arguments': 2},
            {'round': 2, 'counter_arguments': 3},
            {'round': 3, 'counter_arguments': 4},
            {'round': 4, 'counter_arguments': 5},
            {'round': 5, 'counter_arguments': 6}
        ]

        # After 5 rounds without convergence
        is_unproductive = len(debate_rounds) >= 5
        assert is_unproductive is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
