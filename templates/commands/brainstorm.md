---
description: Multi-agent collaborative brainstorming using Team mode with specialized roles and devil's advocate challenge.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Check prerequisites**: Run `{SCRIPT}` to verify feature directory and available documents.

2. **Parse user input**:
   - Extract the `<idea>` argument (one-sentence feature description)
   - Generate short-name from idea (2-4 words, lowercase, hyphenated)
   - Check for `--with-security` flag
   - Check for `--mode {full|quick}` flag (default: full)
   - Check for `--skip-awareness` flag
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

   ### Phase 0: Repository Awareness (NEW)
   - **Before starting proposal preparation, display project repository information**
   - **This phase ensures architects and technical experts understand the project context**

   #### Step 0.1: Extract Repository Information
   ```
   IMPLEMENTATION REQUIRED:

   1. Read README.md (if exists) for:
      - Project name and description
      - Project background and purpose
      - Design principles (if documented)
   2. Scan root directory for tech stack indicators:
      - package.json → Node.js/JavaScript (show dependencies list)
      - pyproject.toml → Python (show dependencies list)
      - go.mod → Go (show dependencies list)
      - Cargo.toml → Rust (show dependencies list)
      - pom.xml → Java (show dependencies list)
   3. Detect core modules and directory structure:
      - List src/, lib/, app/, packages/ directories
      - Identify main entry points (index.js, main.py, main.go, etc.)
      - Show relationship between modules
   4. Check .specify/ directory for SDD configuration files
   5. Scan docs/ directory for architecture documentation (*.md files)
   6. Check for common doc files: CONTRIBUTING.md, ARCHITECTURE.md, DESIGN.md
   7. For each detected tech stack component, note its purpose if documented
   ```

   #### Step 0.2: Display Repository Overview
   ```
   **Mode: Full** (default)
   Display all collected information organized by audience:

   For Technical Expert (US2):
   - Tech stack with version info (from package.json, pyproject.toml, etc.)
   - Key dependencies list (show main dependencies)
   - Core modules and their relationships
   - Entry points (main.py, index.js, main.go, etc.)

   For Architect:
   - Directory structure (src/, lib/, app/, etc.)
   - Architecture documentation paths
   - Design principles (if found)

   For New Members (US3):
   - Project background and purpose
   - Contributing guidelines (CONTRIBUTING.md)
   - Design principles summary

   **Mode: Quick**
   Display only essential information:
   - Project name
   - Project description
   - Detected tech stack (brief)
   - "Press Enter to continue or 'S' to skip detailed view"
   ```

   #### Step 0.3: User Confirmation
   ```
   1. Display: "Please review the project information above"
   2. Options:
      - [Enter] "I have reviewed and understand the project" → Record confirmation → Proceed to Phase 1
      - [S] "Skip awareness phase" → Check .specify/awareness-state.json for user record
         - If record exists: Record skip → Proceed to Phase 1
         - If no record: Display warning "You must complete awareness phase first"
   3. If repository info is incomplete/missing:
      - Display warning: "Some repository information could not be found"
      - List what was found vs what was missing
      - Require explicit confirmation
   ```

   #### Step 0.4: Record Awareness State
   ```
   After user confirmation:

   1. Load .specify/awareness-state.json
   2. Generate userId (use environment: USER or USERNAME)
   3. Update user's record:
      {
        "lastConfirmed": "<ISO-8601 timestamp>",
        "skipCount": <increment if skip used>,
        "preferredMode": "<full|quick>"
      }
   4. Save back to .specify/awareness-state.json
   ```

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
   - Check for specs directory, create if not exists
   - Determine next available spec number (e.g., `004`)
   - Create directory: `specs/<number>-<short-name>/`
   - Generate `specs/<number>-<short-name>/spec.proposal.md` (user stories draft)
     - **Source**: PM + Test Expert contributions
     - **Contains**: User scenarios, user stories, acceptance criteria, priority
     - **No technical details**
   - Generate `specs/<number>-<short-name>/plan.proposal.md` (technical proposal draft)
     - **Source**: Architect + Tech Expert contributions
     - **Contains**: System design, tech stack, risks, integration points
   - Generate `specs/<number>-<short-name>/brainstorm-appendix.md` (full transcript, unchanged)
   - **Create feature branch**: `git checkout -b <number>-<short-name>` to enable seamless specify workflow
   - Present results to user with next steps:
     - "Run `/speckit.specify` to refine spec.proposal.md into final spec"
     - "Run `/speckit.plan` to analyze plan.proposal.md and create technical design"

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

### spec.proposal.md (User Stories Draft)
User stories and requirements extracted from brainstorming. This is what specify refines into final spec.
- User needs and pain points (from PM)
- User scenarios and journeys (from PM, reviewed by Test)
- User stories with priorities
- Acceptance criteria (from Test)
- Business value and ROI considerations

**IMPORTANT**: This contains no technical details - only user-facing requirements.

### plan.proposal.md (Technical Proposal Draft)
Technical architecture and implementation considerations extracted from brainstorming. This is what plan analyzes and expands.
- System design proposals (from Architect)
- Technology selection options (from Tech Expert)
- Scalability and reliability considerations (from Architect)
- Implementation risks and constraints (from Tech Expert)
- Integration points and dependencies
- Non-functional requirements (DFX)

**NOTE**: This is raw technical input for plan - plan will analyze, validate, and expand into detailed design.

### Appendix: brainstorm-appendix.md (Full Technical Analysis)
Comprehensive technical analysis preserved for reference:
- Chronological debate transcript
- All role proposals (verbatim)
- All counter-arguments and challenges
- Risk assessments
- Architecture options with pros/cons
- All decisions with rationale
- Technical considerations (scalability, security, performance)

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
