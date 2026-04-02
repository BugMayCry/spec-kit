# Tasks: Brainstorm仓库认知增强

**Input**: Design documents from `/specs/004-brainstorm-repo-awareness/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Tests**: Not explicitly requested in spec - skipping test tasks

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Review existing brainstorm.md template at templates/commands/brainstorm.md
- [x] T002 [P] Review existing spec-template.md at templates/spec-template.md
- [x] T003 [P] Review contracts/brainstorm-awareness.md for interface details

**Checkpoint**: Ready to begin template modifications

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Define awareness state schema in .specify/awareness-state.json
- [x] T005 [P] Implement awareness state read/write functions in src/specify_cli/
- [x] T006 [P] Implement repository info extraction logic (README, tech stack, dir structure)

---

## Phase 3: User Story 1 - 架构师在提案前审查仓库 (Priority: P1) 🎯 MVP

**Goal**: 架构师执行brainstorm命令时，系统强制展示仓库关键信息，确认后方可进入提案准备阶段

**Independent Test**: 执行brainstorm命令时，系统首先展示仓库认知页面，用户必须确认才能继续

### Implementation for User Story 1

- [x] T007 [P] [US1] Add --mode parameter handling in templates/commands/brainstorm.md
- [x] T008 [P] [US1] Add repository awareness display section in templates/commands/brainstorm.md
- [x] T009 [US1] Add user confirmation flow in templates/commands/brainstorm.md
- [x] T010 [US1] Integrate awareness state recording after confirmation
- [x] T011 [US1] Add warning when repo info is incomplete in templates/commands/brainstorm.md

**Checkpoint**: At this point, User Story 1 should be fully functional

---

## Phase 4: User Story 2 - 技术专家验证方案可行性 (Priority: P2)

**Goal**: 技术专家可以看到现有技术栈、核心模块和依赖关系

**Independent Test**: 技术专家执行brainstorm时能看到项目中已有的技术组件和代码组织方式

### Implementation for User Story 2

- [ ] T012 [P] [US2] Enhance repository info extraction to include tech stack detection
- [ ] T013 [P] [US2] Add core modules and dependencies display in templates/commands/brainstorm.md
- [ ] T014 [US2] Add component linking when expert references existing components

**Checkpoint**: User Story 2 complete - tech experts can verify feasibility

---

## Phase 5: User Story 3 - 新成员快速了解项目背景 (Priority: P3)

**Goal**: 新成员可以通过brainstorm命令快速了解项目背景和设计原则

**Independent Test**: 新成员执行brainstorm时能看到项目背景文档和架构设计说明

### Implementation for User Story 3

- [ ] T015 [P] [US3] Add project background doc detection (README, docs/)
- [ ] T016 [P] [US3] Add architecture design principles display in templates/commands/brainstorm.md
- [ ] T017 [US3] Record awareness completion state for new members

**Checkpoint**: User Story 3 complete - new members can onboard quickly

---

## Phase 6: User Story 4 - 提案与正式规范区分 (Priority: P2)

**Goal**: Brainstorm生成的spec.md文件采用双重标识（文件名+Status）标记为"提案"

**Independent Test**: 执行brainstorm后生成的文档具有明确的"提案"标识

### Implementation for User Story 4

- [x] T018 [P] [US4] Modify spec filename generation to add "proposal-" prefix
- [x] T019 [P] [US4] Modify Status field to set "Proposal" in generated spec
- [ ] T020 [US4] Verify dual identification works correctly

**Checkpoint**: User Story 4 complete - proposals clearly distinguished from specs

---

## Phase 7: User Story 5 - 跳过与模式选择 (Priority: P2)

**Goal**: 已确认用户可跳过认知阶段；用户可选择完整模式或快速模式

**Independent Test**: 已确认用户执行brainstorm时可选择跳过；用户可选择不同模式

### Implementation for User Story 5

- [ ] T021 [P] [US5] Implement --skip-awareness parameter in templates/commands/brainstorm.md
- [ ] T022 [P] [US5] Implement skip validation (check awareness-state.json)
- [ ] T023 [P] [US5] Implement quick mode display (core info only) vs full mode
- [ ] T024 [US5] Record skip usage in awareness-state.json

**Checkpoint**: User Story 5 complete - skip and mode selection work

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T025 [P] Update README.md with new brainstorm parameters
- [ ] T026 [P] Add examples for --mode and --skip-awareness in help text
- [ ] T027 Validate all templates render correctly
- [ ] T028 Run quickstart.md validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✓
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: MVP - Core awareness flow - starts after Foundational
- **US2 (P2)**: Depends on US1 core flow
- **US3 (P3)**: Depends on US1 core flow
- **US4 (P2)**: Independent - can run parallel with US2/US3
- **US5 (P2)**: Depends on US1 (skip needs core flow)

### Within Each User Story

- Core flow before edge cases
- Different display sections marked [P] can run in parallel
- Integration at the end

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel ✓
- Foundational tasks marked [P] can run in parallel
- US1, US2, US3, US4, US5 can be worked on in parallel after Foundational
- Different template sections marked [P] within each story

---

## MVP Scope (User Story 1 Only)

To ship MVP:

1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Partial - T010 remaining)
4. **STOP and VALIDATE**: Test awareness flow works
5. Deploy/demo if ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- This is a template-only project - implementation is in markdown templates
- Commit after each phase or logical group
