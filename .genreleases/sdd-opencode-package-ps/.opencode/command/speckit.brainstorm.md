---
description: Multi-agent collaborative brainstorming using Team mode with specialized roles and devil's advocate challenge.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Check prerequisites**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` to verify feature directory and available documents.

2. **Parse user input**:
   - Extract the `<idea>` argument (one-sentence feature description)
   - Check for `--with-security` flag
   - If no idea provided: Prompt user for clarification (EC-002)

3. **Check Team mode availability**:
   ```python
   import os
   team_mode_enabled = os.getenv("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"
   ```
   - If not enabled: Display warning, offer lite mode (EC-001)
   - If enabled: Proceed with Team mode

4. **Determine active roles**:
   | Role | Member ID | Condition |
   |------|-----------|-----------|
   | Product Manager | `member-pm` | Always |
   | Architect | `member-architect` | Always |
   | Technical Expert | `member-tech` | Always |
   | Test Expert | `member-test` | Always |
   | Security Expert | `member-security` | Only with `--with-security` |
   | Devil's Advocate | `member-devil` | Debate phase only |

5. **Execute brainstorming workflow**:

   ### Phase 1: Proposal Collection
   - Spawn Team Members for each active role
   - Send `propose` message to each member with:
     - User's idea as context
     - Role-specific instructions
   - Collect `proposal` responses from each role
   - Store proposals in memory

   ### Phase 2: Debate (with Devil's Advocate)
   - Spawn `member-devil` for debate phase
   - Send `debate` message to all members with proposals
   - Collect `counter_argument` messages
   - Track contested vs unanimous points
   - For contested points: Request multiple options with pros/cons

   ### Phase 3: Decision
   - For each contested point:
     - Send `decision_request` to user
     - Wait for user `decision` message
   - Record decisions in Decisions Log

   ### Phase 4: Output
   - Generate `spec.md` from proposals and decisions
   - Generate `brainstorm-appendix.md` with full transcript
   - Present results to user

6. **Fallback to Lite Mode** (if Team mode unavailable):
   - Run in single-agent mode
   - Sequentially prompt each role's perspective
   - Skip real-time debate
   - Merge into spec without interactive decision

---

## Role Instructions

### Product Manager (member-pm)
Focus on:
- User needs and pain points
- Business value and ROI
- Priority and success metrics
- User stories and acceptance criteria

### Architect (member-architect)
Focus on:
- System design and structure
- Non-functional requirements (DFX)
- Scalability and reliability
- Integration points

### Technical Expert (member-tech)
Focus on:
- Technology selection
- Feasibility analysis
- Technical constraints
- Implementation risks

### Test Expert (member-test)
Focus on:
- Acceptance criteria testability
- Test scenarios and edge cases
- Quality gates
- Verification approach

### Security Expert (member-security)
Focus on:
- Security threats and attack vectors
- Compliance requirements (GDPR, SOC2, etc.)
- Data protection and privacy
- Security acceptance criteria

### Devil's Advocate (member-devil)
Challenge every assumption:
- "What could go wrong?"
- "What are the single points of failure?"
- "Is this scalability claim justified?"
- "What edge cases are being ignored?"

---

## Message Types

### propose (Team Lead → Role)
```json
{
  "type": "propose",
  "role": "<role_id>",
  "context": "<user's idea>",
  "instructions": "<role-specific instructions>"
}
```

### proposal (Role → Team Lead)
```json
{
  "type": "proposal",
  "role": "<role_id>",
  "content": "# <Role> Proposal\n\n...",
  "key_points": ["point1", "point2"],
  "risks": ["risk1", "risk2"],
  "questions": ["question1"]
}
```

### debate (Team Lead → All)
```json
{
  "type": "debate",
  "phase": "cross_examination",
  "proposals": { ... }
}
```

### counter_argument (Role → Team Lead)
```json
{
  "type": "counter_argument",
  "target_role": "<role_id>",
  "target_point": "<point being challenged>",
  "argument": "<challenge text>",
  "suggestion": "<alternative or question>"
}
```

### decision_request (Team Lead → User)
```json
{
  "type": "decision_request",
  "topic": "<contested topic>",
  "options": [
    {"option": "A", "pros": [...], "cons": [...]},
    {"option": "B", "pros": [...], "cons": [...]}
  ]
}
```

### decision (User → Team Lead)
```json
{
  "type": "decision",
  "topic": "<contested topic>",
  "choice": "A",
  "rationale": "<optional reason>"
}
```

---

## Output Format

### spec.md Sections
- Executive Summary (from PM + Architect)
- User Scenarios (from PM, reviewed by Test)
- Functional Requirements (from PM + Tech Expert)
- Non-Functional Requirements (from Architect + Security)
- Acceptance Criteria (from Test Expert)
- Risks & Mitigations (from Devil's Advocate challenges)
- Decisions Log (from user decisions)

### Appendix: brainstorm-appendix.md
- Chronological debate transcript
- All proposals (verbatim)
- All counter-arguments
- All decisions with rationale

---

## Edge Cases

| Code | Scenario | Handling |
|------|----------|-----------|
| EC-001 | Team mode not enabled | Display warning, offer lite mode |
| EC-002 | Empty/vague idea | Prompt for clarification |
| EC-003 | Unanimous agreement | Skip debate, proceed to spec |
| EC-004 | Security concerns mid-debate | Offer to invite security expert |
| EC-005 | Debate unproductive | Allow user intervention |

---

## Success Criteria Validation

| SC | Metric | Target |
|----|--------|--------|
| SC-001 | Proposal generation time | < 5 min |
| SC-002 | Devil's advocate challenge rate | ≥ 3 challenges/major assumption |
| SC-003 | Debate resolution | ≤ 2 rounds |
| SC-004 | spec.md completeness | All sections populated |
| SC-005 | Appendix completeness | No messages omitted |
| SC-006 | Completeness score | ≥ 80% |
