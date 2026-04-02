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

   1. Read README.md (if exists) for project overview and description
   2. Scan root directory for tech stack indicators:
      - package.json → Node.js/JavaScript
      - pyproject.toml → Python
      - go.mod → Go
      - Cargo.toml → Rust
      - pom.xml → Java
      - *.csproj → C#/.NET
   3. Check .specify/ directory for SDD configuration files
   4. Scan docs/ directory for architecture documentation (*.md files)
   5. Detect top-level directory structure (list root folders)
   6. Check for common doc files: CONTRIBUTING.md, ARCHITECTURE.md, DESIGN.md
   ```

   #### Step 0.2: Display Repository Overview
   ```
   **Mode: Full** (default)
   Display all collected information:
   - Project name (from README or directory name)
   - Project description (first paragraph of README)
   - Detected tech stack (list all found)
   - Architecture documentation paths
   - Directory structure (top-level folders)
   - All available documentation files

   **Mode: Quick**
   Display only essential information:
   - Project name
   - Project description
   - Detected tech stack
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
   - Generate `specs/<number>-<short-name>/spec.md` (concise draft for specify)
     - **IMPORTANT**: Replace `$STATUS` in the generated spec with `Proposal`
     - Filename format: `proposal-<number>-<short-name>-spec.md` (note: "proposal-" prefix)
   - Generate `specs/<number>-<short-name>/brainstorm-appendix.md` (full technical analysis)
   - **Create feature branch**: `git checkout -b <number>-<short-name>` to enable seamless specify workflow
   - Present results to user with next steps and remind them they can now run `/speckit.specify` to continue

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

### spec.md (Concise Draft for Specify)
A clean, concise spec that specify can understand and refine. Include only:
- Feature name and brief description
- Key decisions already made (with rationale)
- Open questions for specify to explore
- High-level user scenarios

**IMPORTANT**: Keep this minimal. Do NOT include technical details here - they belong in the appendix.

### Appendix: brainstorm-appendix.md (Full Technical Analysis)
Comprehensive technical analysis preserved for reference by specify/plan:
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
