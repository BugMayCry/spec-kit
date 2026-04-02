# Implementation Plan: Multi-Agent Collaborative Brainstorming

**Branch**: `003-brainstorm-team-collab` | **Date**: 2026-04-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `./spec.md`

## Summary

Extend spec-kit with `/speckit.brainstorm` command that uses Claude Code Team mode to enable multi-agent collaborative specification writing. Five specialized roles (Product Manager, Architect, Technical Expert, Test Expert, Devil's Advocate) work together with user as Product Owner making final decisions on contested points.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Agent tool (Team mode), SendMessage, typer, rich
**Storage**: JSON files (team-config.json), Markdown files (spec.md, appendix)
**Testing**: pytest
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: CLI command extension - modifying existing `templates/commands/`
**Performance Goals**: Role proposal generation within 5 minutes
**Constraints**: Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, fallback to lite mode if unavailable
**Scale/Scope**: Designed for medium-to-large features (2+ user stories)

## Constitution Check

*Note: constitution.md is still a template with placeholders. No gates to evaluate.*

## Project Structure

### Documentation (this feature)

```text
specs/003-brainstorm-team-collab/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (if needed)
├── data-model.md        # Phase 1 output (if needed)
├── quickstart.md        # Phase 1 output (if needed)
├── contracts/           # Phase 1 output (if needed)
└── tasks.md            # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
templates/commands/
└── brainstorm.md        # NEW: Main slash command implementation

.specify/
└── team-config.json    # RUNTIME: Team member tracking (gitignored)
```

**Structure Decision**: Single command file `brainstorm.md` in `templates/commands/`, following existing pattern for `/speckit.specify`, `/speckit.implement` etc.

## Implementation Approach

### Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Team mode integration | Agent tool with team_name and name params | Native Team mode support |
| Message passing | SendMessage with JSON payloads | Structured communication |
| Fallback mode | Sequential role prompts (lite mode) | When Team mode unavailable |
| Output format | Markdown (spec.md + appendix) | Native spec-kit format |

### Communication Protocol

**Message Types**:
- `propose`: Team Lead → Role (request for proposal)
- `proposal`: Role → Team Lead (structured proposal response)
- `debate`: Team Lead → All (initiate debate phase)
- `counter_argument`: Role → Team Lead (challenge to another role's point)
- `decision_request`: Team Lead → User (request for decision)
- `decision`: User → Team Lead (final decision)

### Role Configuration

| Role | Member ID | Spawn Condition |
|------|-----------|-----------------|
| Product Manager | `member-pm` | Always |
| Architect | `member-architect` | Always |
| Technical Expert | `member-tech` | Always |
| Test Expert | `member-test` | Always |
| Security Expert | `member-security` | Only with `--with-security` flag |
| Devil's Advocate | `member-devil` | Debate phase only |

## Complexity Tracking

*No complexity violations.*

---

## Phase 0: Research (Minimal)

*This feature primarily extends existing CLI commands with Team mode integration. No extensive research needed.*

### Research Tasks

| Task | Status | Notes |
|------|--------|-------|
| Team mode Agent tool usage patterns | DONE | Covered by design doc |
| SendMessage protocol best practices | DONE | Covered by design doc |
| Lite mode fallback implementation | DONE | Sequential prompts, no Team needed |

**Conclusion**: No additional research required. Proceed to Phase 1.

---

## Phase 1: Design & Contracts

### 1.1 Data Model

**Not applicable**: This feature modifies CLI workflow, not data storage. Entity definitions in spec.md are sufficient:
- Proposal: Conceptually defined, no persistence needed
- Decision: Recorded in spec appendix, not stored
- DebateRecord: Kept in memory, output as appendix

### 1.2 Contracts

**Team Communication Protocol** (defined in design doc):
- Standard message envelope with type, from, to, payload
- Proposal structure: role, content, key_points, risks, questions
- Decision structure: topic, choice, rationale

**CLI Interface**:
```
/speckit.brainstorm <idea> [--with-security]
```

### 1.3 Quickstart

**For Testing**:
1. Ensure `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
2. Run `/speckit.brainstorm Build a user authentication system`
3. Observe role proposals and debate
4. Make decisions on contested points
5. Review generated spec.md and appendix

---

## Rollout Plan

1. **Phase 1**: Create `templates/commands/brainstorm.md` with core command structure
2. **Phase 2**: Implement Team member spawning and proposal collection
3. **Phase 3**: Implement debate phase with devil's advocate
4. **Phase 4**: Implement user decision flow
5. **Phase 5**: Implement lite mode fallback
6. **Phase 6**: Testing and polish
