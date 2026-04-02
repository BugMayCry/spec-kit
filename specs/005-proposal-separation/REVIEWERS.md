# Review Summary: Split Brainstorm Output

**Spec:** specs/005-proposal-separation/spec.md | **Plan:** specs/005-proposal-separation/plan.md
**Generated:** 2026-04-02

---

## Executive Summary

This feature improves the speckit brainstorming workflow by separating output into two distinct proposal files:
- `spec.proposal.md` - User stories from PM + Test roles
- `plan.proposal.md` - Technical proposals from Architect + Tech roles

Currently, brainstorm generates a single `spec.md` that mixes user-facing requirements with technical details. This makes it harder for PMs to iterate on user stories independently and forces technical content into what should be a business-focused document.

The change modifies three command templates:
1. `brainstorm.md` - Output format changes
2. `specify.md` - Reads from spec.proposal.md
3. `plan.md` - Analyzes plan.proposal.md

This is a workflow improvement, not a code implementation.

---

## Review Recipe (30 minutes)

### Step 1: Understand the problem (5 min)
- Read the Executive Summary above
- Review FR-001 through FR-006 in spec.md
- Ask: Is the separation of user stories from technical proposals valuable?

### Step 2: Check critical references (10 min)
- Review spec.md Section: Proposal File Structures (defines the two file formats)
- Review plan.md Section: Implementation Details (exact changes to each template)
- Review Edge Cases section in spec.md

### Step 3: Evaluate technical decisions (8 min)
- Backward compatibility decision (fallback mechanism)
- File structure decision (separate files vs sections in one file)
- Plan requires plan.proposal.md (no fallback)

### Step 4: Validate coverage and risks (5 min)
- Check that all 6 FRs have implementing tasks
- Review Risk Areas table below
- Verify edge cases are covered

### Step 5: Complete the checklist (2 min)
- Work through the Reviewer Checklist below

---

## PR Contents

| Artifact | Description |
|---------|-------------|
| `spec.md` | Feature specification with 3 user stories, 6 functional requirements |
| `plan.md` | Implementation plan with 3 template file modifications |
| `tasks.md` | 23 validation tasks across 5 phases |
| `REVIEWERS.md` | This file |

---

## Technical Decisions

### Decision 1: Dual File Output
- **Chosen approach:** Separate spec.proposal.md and plan.proposal.md files
- **Alternatives considered:**
  - Single file with section headers: Rejected because specify and plan need distinct inputs
  - ID-based referencing: Rejected as over-engineering (Devil's Advocate raised this)
- **Trade-off:** Clear separation vs additional file management
- **Reviewer question:** Is the file count increase acceptable to users?

### Decision 2: Backward Compatibility
- **Chosen approach:** specify command fallback to spec.md when spec.proposal.md missing
- **Alternatives considered:**
  - Require both files: Rejected - would break existing workflows
  - Versioned format: Deferred to future iteration
- **Trade-off:** Compatibility vs added complexity in specify command
- **Reviewer question:** Is the fallback behavior clear enough?

### Decision 3: plan Requires plan.proposal.md
- **Chosen approach:** plan command errors if plan.proposal.md missing
- **Alternatives considered:**
  - Fallback to spec.md for tech content: Rejected - spec lacks technical depth
  - Auto-generate template: Deferred
- **Trade-off:** User experience vs technical completeness

---

## Critical References

| Reference | Why it needs attention |
|----------|----------------------|
| `spec.md` Section: Proposal File Structures | Defines exact content of each proposal file |
| `spec.md` Section: Edge Cases | Defines fallback and error behaviors |
| `plan.md` Section: Implementation Details | Exact changes to each template file |
| `spec.md` FR-004 | specify fallback behavior is critical for migration |

---

## Reviewer Checklist

### Verify
- [ ] All 6 functional requirements have corresponding validation tasks
- [ ] Edge cases cover: missing spec.proposal.md, missing plan.proposal.md, empty files
- [ ] Tasks include exact file paths for all template modifications
- [ ] Backward compatibility is tested (T014)

### Question
- [ ] Is the dual-file structure intuitive for new users?
- [ ] Should plan.proposal.md also have a fallback mechanism?

### Watch out for
- [ ] Users may not understand the difference between spec.proposal.md and spec.md
- [ ] Migration from old format may need documentation

---

## Scope Boundaries

- **In scope:** Template modifications, E2E validation tasks
- **Out of scope:** Code implementation, library changes
- **Why these boundaries:** This is a workflow improvement, not a feature requiring code

---

## Risk Areas

| Risk | Impact | Mitigation |
|------|--------|------------|
| Users don't understand new file structure | Medium | Clear documentation in command help |
| Old projects need migration | Low | Fallback mechanism + migration guide (T022) |
| Role boundaries unclear during brainstorming | Medium | Defined chapter structures in spec |

---

*Share this with reviewers. Full context in linked spec and plan.*
