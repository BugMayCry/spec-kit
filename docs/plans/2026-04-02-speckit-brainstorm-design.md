# /speckit.brainstorm Design

**Date**: 2026-04-02
**Author**: Claude Code
**Status**: Approved

---

## Overview

`/speckit.brainstorm` is a new slash command that uses Claude Code Team mode to enable multi-agent collaborative ideation. Multiple specialized roles (product manager, architect, technical expert, test expert, security compliance expert) work together with a dedicated devil's advocate to challenge assumptions and produce high-quality specifications.

---

## Problem Statement

Single-agent specification writing often suffers from:
- Blind spots due to limited perspective
- Unchallenged assumptions
- Missing non-functional requirements
- Lack of diverse domain expertise
- Requirements that are difficult to test

---

## Solution

A Team-based brainstorming command where multiple specialized agents collaboratively develop a spec, with a dedicated "devil's advocate" role that challenges every assumption to ensure robustness.

---

## Role Definitions

### Core Roles (Always Participated)

| Role | Responsibilities |
|------|------------------|
| **Product Manager** | Business value, user needs, priority, success metrics |
| **Architect** | System design, technical architecture, DFX (performance, reliability, scalability, maintainability) |
| **Technical Expert** | Technology selection, feasibility analysis, constraint identification |
| **Test Expert** | Acceptance criteria, testability, test strategy, quality thresholds |

### Optional Role

| Role | Trigger | Responsibilities |
|------|---------|------------------|
| **Security Compliance Expert** | `--with-security` flag | Security threat modeling, compliance (GDPR/SOC2), data protection, privacy |

### Special Role

| Role | When to Join | Responsibilities |
|------|---------------|------------------|
| **Devil's Advocate** | Debate phase only | Challenge assumptions, find flaws, break groupthink |

---

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. User Input                                              │
│     User provides a one-sentence idea                         │
│     e.g., "/speckit.brainstorm Build a payment system"      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Independent Proposal Phase                               │
│     Each core role independently develops their proposal:     │
│     - PM → User needs & business requirements               │
│     - Architect → System architecture & DFX                 │
│     - Technical Expert → Technology & feasibility            │
│     - Test Expert → Acceptance criteria & testability         │
│     (Security Expert joins if --with-security specified)      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Debate Phase                                            │
│     - Devil's Advocate joins the team                       │
│     - Roles debate via Team SendMessage                      │
│     - Devil's Advocate challenges assumptions               │
│     - Unresolvable disagreements → multiple options + pros/cons │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Decision Phase                                           │
│     User (as Product Owner) reviews:                         │
│     - All proposals                                          │
│     - Debate outcomes                                        │
│     - Multiple options with tradeoffs (where applicable)     │
│     User makes final decisions on contested points           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Output                                                   │
│     - spec.md (ready for /speckit.plan)                     │
│     - Appendix: Full debate transcript                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Command Interface

### Invocation

```
/speckit.brainstorm <one-sentence-idea> [--with-security]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `<idea>` | Required. A one-sentence description of the feature |
| `--with-security` | Optional. Include Security Compliance Expert |

### Example

```
/speckit.brainstorm Build a real-time collaborative document editing system --with-security
```

---

## Team Configuration

### Team Structure

- **Team Lead**: The main Claude Code session (facilitates and makes decisions)
- **Team Members**: Specialized roles spawned via Agent tool

### Member Naming Convention

| Role | Member ID |
|------|-----------|
| Product Manager | `member-pm` |
| Architect | `member-architect` |
| Technical Expert | `member-tech` |
| Test Expert | `member-test` |
| Security Expert | `member-security` |
| Devil's Advocate | `member-devil` |

---

## Communication Protocol

### Message Types

#### Team Lead → Member: `propose`
```json
{
  "type": "propose",
  "role": "architect",
  "context": "User idea: Build a real-time collaborative editing system",
  "instructions": "Please develop your proposal for system architecture..."
}
```

#### Member → Team Lead: `proposal`
```json
{
  "type": "proposal",
  "role": "architect",
  "content": "# Architecture Proposal\n\n## System Design...",
  "key_points": ["point1", "point2"],
  "risks": ["risk1", "risk2"],
  "questions": ["question1"]
}
```

#### Team Lead → All: `debate`
```json
{
  "type": "debate",
  "phase": "cross_examination",
  "proposals": { ... }
}
```

#### Member → Team Lead: `counter_argument`
```json
{
  "type": "counter_argument",
  "target_role": "architect",
  "target_point": "microservices_architecture",
  "argument": "Why microservices may be overkill...",
  "suggestion": "Consider a modular monolith instead"
}
```

#### Team Lead → All: `decision_request`
```json
{
  "type": "decision_request",
  "contested_points": [
    {
      "topic": "architecture_style",
      "options": [
        {"option": "A", "pros": [...], "cons": [...]},
        {"option": "B", "pros": [...], "cons": [...]}
      ]
    }
  ]
}
```

#### User → Team Lead: `decision`
```json
{
  "type": "decision",
  "topic": "architecture_style",
  "choice": "A",
  "rationale": "..." // optional
}
```

---

## Output Format

### Main Output: spec.md

The primary output follows the standard spec-kit spec.md template with contributions from all roles:

```markdown
# Feature Specification: <Feature Name>

## Executive Summary
<High-level description from PM + Architect>

## User Scenarios
<User stories from PM, reviewed by Test Expert>

## Functional Requirements
<From PM and Technical Expert>

## Non-Functional Requirements
<From Architect (DFX) and Security Expert (if present)>

## Acceptance Criteria
<From Test Expert, reviewed by all>

## Risks & Mitigations
<From Devil's Advocate challenges, addressed by relevant experts>

## Decisions Log
<Final decisions made by Product Owner>
```

### Appendix: Debate Transcript

Full chronological record of all messages exchanged during the debate phase, including:
- Initial proposals from each role
- Cross-examination and counter-arguments
- Unanimous agreements
- Contested points and resolution options
- Product Owner decisions

---

## Implementation Notes

### Team Mode Requirement

This feature requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable. If not set:
- Display warning that Team mode is required
- Offer to proceed in "lite" mode (sequential single-agent brainstorming)

### Fallback Behavior

If Team mode is unavailable:
- Run in single-agent mode with role perspectives prompted sequentially
- Reduce interactive debate
- Produce spec.md with explicit "single-agent mode" notation

### Debate Moderation

Team Lead (this session) acts as moderator:
- Ensures all voices are heard
- Tracks which points are contested vs unanimous
- Requests decisions from Product Owner when needed
- Summarizes and synthesizes proposals

### Devil's Advocate Strategy

The devil's advocate role specifically:
- Challenges every assumption stated as fact
- Asks "what could go wrong?"
- Identifies single points of failure
- Questions scalability claims
- Probes edge cases and boundary conditions

---

## File Structure

```
templates/commands/
├── brainstorm.md              # Main slash command implementation
└── ...

docs/plans/
└── 2026-04-02-speckit-brainstorm-design.md  # This document
```

---

## Future Enhancements

- [ ] Support for custom role combinations
- [ ] Integration with existing spec.md for enhancement projects
- [ ] Debate summary visualization
- [ ] Historical debate archive for similar features
- [ ] LLM-generated decision rationale suggestions

---

## Approval

- **Date**: 2026-04-02
- **Approver**: Product Owner
- **Status**: Ready for Implementation
