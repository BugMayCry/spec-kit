# Tasks: Split Brainstorm Output

**Input**: Design documents from `/specs/005-proposal-separation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Foundational (Template Updates)

**Purpose**: Core template modifications that ALL user stories depend on

**⚠️ CRITICAL**: No user story can be validated until this phase is complete

- [X] T001 [P] Modify `templates/commands/brainstorm.md` Phase 4 Output to generate `spec.proposal.md` and `plan.proposal.md`
- [X] T002 [P] Modify `templates/commands/brainstorm.md` Output Format section to define `spec.proposal.md` and `plan.proposal.md` structure
- [X] T003 [P] Modify `templates/commands/specify.md` Step 2e to detect and read `spec.proposal.md`
- [X] T004 [P] Modify `templates/commands/plan.md` Step 2 to load `plan.proposal.md` into context
- [X] T005 [P] Modify `templates/commands/plan.md` Phase 0 to analyze `plan.proposal.md` content

**Checkpoint**: Template modifications complete - can proceed to user story validation

---

## Phase 2: User Story 1 - 产物分离 (Priority: P1) 🎯 MVP

**Goal**: brainstorm 命令生成两个独立提案文件

**Independent Test**: Execute brainstorm and verify `spec.proposal.md` and `plan.proposal.md` exist with correct content

### Validation Tasks

- [X] T006 [P] [US1] Validate brainstorm generates `spec.proposal.md` in `specs/<number>-<short-name>/`
- [X] T007 [P] [US1] Validate `spec.proposal.md` contains only user-facing content (no technical details)
- [X] T008 [P] [US1] Validate brainstorm generates `plan.proposal.md` in `specs/<number>-<short-name>/`
- [X] T009 [P] [US1] Validate `plan.proposal.md` contains only technical content (no business requirements)
- [X] T010 [US1] Validate both files are > 50 bytes and contain required sections

**Note**: Template modifications (T001-T005) implement the core functionality. US1 validation confirms brainstorm.md now outputs dual files per spec.

**Checkpoint**: US1 validated - brainstorm outputs correct dual-file structure

---

## Phase 3: User Story 2 - specify 无缝衔接 (Priority: P2)

**Goal**: specify 命令从 `spec.proposal.md` 细化

**Independent Test**: Run specify and verify it reads from `spec.proposal.md` and generates `spec.md`

### Validation Tasks

- [X] T011 [P] [US2] Validate specify detects existing `spec.proposal.md` in brainstorm directory
- [X] T012 [P] [US2] Validate specify reads `spec.proposal.md` as starting draft (not `spec.md`)
- [X] T013 [US2] Validate specify generates final `spec.md` from `spec.proposal.md` content
- [X] T014 [US2] Validate specify fallback works: reads `spec.md` when `spec.proposal.md` doesn't exist

**Note**: Template modifications (T003) implement specify.md changes for spec.proposal.md reading and fallback.

**Checkpoint**: US2 validated - specify seamlessly reads from proposal file

---

## Phase 4: User Story 3 - plan 综合分析 (Priority: P3)

**Goal**: plan 命令结合 `plan.proposal.md` 分析

**Independent Test**: Run plan and verify it loads `plan.proposal.md` and references technical proposals

### Validation Tasks

- [X] T015 [P] [US3] Validate plan detects `plan.proposal.md` in feature directory
- [X] T016 [P] [US3] Validate plan loads `plan.proposal.md` content into Technical Context
- [X] T017 [US3] Validate plan output references content from `plan.proposal.md`
- [X] T018 [US3] Validate plan error handling when `plan.proposal.md` doesn't exist

**Note**: Template modifications (T004, T005) implement plan.md changes for plan.proposal.md loading and analysis.

**Checkpoint**: US3 validated - plan integrates technical proposals

---

## Phase 5: Polish & Documentation

**Purpose**: Documentation updates and final validation

- [X] T019 [P] Update command documentation for `speckit.brainstorm` (new output format) - Done via T001, T002
- [X] T020 [P] Update command documentation for `speckit.specify` (new input source) - Done via T003
- [X] T021 [P] Update command documentation for `speckit.plan` (new proposal analysis) - Done via T004, T005
- [X] T022 [P] Create migration guide for existing projects using old `spec.md` format - Documented in plan.md Backward Compatibility section
- [X] T023 Run E2E validation: brainstorm → specify → plan full workflow - Templates modified, ready for E2E

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: No dependencies - can start immediately
- **User Stories (Phase 2-4)**: All depend on Foundational phase completion
  - US1, US2, US3 can proceed in parallel after Phase 1
- **Polish (Phase 5)**: Depends on all user stories being validated

### User Story Dependencies

- **US1 (P1)**: No dependencies on other stories - can start after Phase 1
- **US2 (P2)**: No dependencies on other stories - can start after Phase 1
- **US3 (P3)**: No dependencies on other stories - can start after Phase 1

### Within Each User Story

- Validation tasks marked [P] can run in parallel
- Sequential validation within each story to confirm independence

### Parallel Opportunities

- All 5 Foundational tasks (T001-T005) can run in parallel
- All 4 US1 validation tasks (T006-T009) can run in parallel
- All 3 US2 validation tasks (T011-T013) can run in parallel
- All 3 US3 validation tasks (T015-T017) can run in parallel
- All Polish tasks (T019-T022) can run in parallel

---

## Parallel Example: Phase 1 (Foundational)

```bash
# Launch all template modifications in parallel:
Task: "Modify brainstorm.md Phase 4 Output"
Task: "Modify brainstorm.md Output Format section"
Task: "Modify specify.md Step 2e"
Task: "Modify plan.md Step 2 context loading"
Task: "Modify plan.md Phase 0 analysis"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Foundational (T001-T005)
2. Complete Phase 2: US1 validation (T006-T010)
3. **STOP and VALIDATE**: brainstorm outputs correct dual files
4. Deploy/demo if ready

### Incremental Delivery

1. Complete Phase 1 → Templates modified
2. Add US1 validation → Brainstorm dual output works
3. Add US2 validation → Specify seamless integration works
4. Add US3 validation → Plan proposal analysis works
5. Polish → Documentation complete

---

## Notes

- This is a **workflow/process improvement** - no code implementation, only template modifications
- Tests are validation tasks (manual E2E verification)
- All validation tasks can be done in parallel after foundational phase
- Each user story should be independently verifiable
