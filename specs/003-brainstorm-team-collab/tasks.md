# Tasks: Multi-Agent Collaborative Brainstorming

**Input**: Implementation plan from `plan.md`
**Prerequisites**: plan.md (required), spec.md (required)
**Organization**: Tasks are grouped by user story - TEST tasks before IMPLEMENT tasks for each story
**TDD Approach**: For each user story, complete all test tasks before implementing features

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Prepare the command template structure and test infrastructure

- [X] T001 Create contracts/team-protocol.md documenting message types and protocol
- [X] T002 Create data-model.md with Proposal, Decision, DebateRecord entities
- [X] T003 Create quickstart.md with usage guide

---

## Phase 2: Foundational (Core Command Infrastructure)

**Purpose**: Core infrastructure that enables the brainstorm command

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Foundational - Implementation

- [ ] T004 [P] Implement `/speckit.brainstorm` command skeleton in templates/commands/brainstorm.md
  - Add command parsing for `<idea>` argument
  - Add `--with-security` flag handler
  - Add CLI help text and usage guide
- [ ] T005 [P] Implement team mode availability detection
  - Check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable
  - Implement fallback to lite mode when Team mode unavailable (EC-001)
- [ ] T006 [P] Define role configurations in templates/commands/brainstorm.md
  - Product Manager: member-pm
  - Architect: member-architect
  - Technical Expert: member-tech
  - Test Expert: member-test
  - Security Expert: member-security (when --with-security)
  - Devil's Advocate: member-devil (debate phase only)

---

## Phase 3: User Story 1 - Multi-Role Brainstorming (Priority: P1) 🎯 MVP

**Goal**: Enable multiple specialized agents to independently generate proposals for a feature

**Independent Test**: Run `/speckit.brainstorm <idea>` and verify each role generates a structured proposal

### User Story 1 - Tests FIRST (TDD)

- [ ] T007 [US1] Add unit tests for role proposal structure validation in tests/test_brainstorm_us1.py
  - Test Proposal model fields: role, content, key_points, risks, questions
  - Test Proposal serialization/deserialization
  - Test invalid role rejection
- [ ] T008 [US1] Add unit tests for team member spawning logic in tests/test_brainstorm_us1.py
  - Test spawn conditions for each role (always vs flag-based)
  - Test member ID generation (member-pm, member-architect, etc.)
  - Test security expert spawn only with --with-security flag
- [ ] T009 [US1] Add unit tests for proposal message handling in tests/test_brainstorm_us1.py
  - Test propose message structure
  - Test proposal message parsing
  - Test timeout handling
- [ ] T010 [US1] Add integration tests for Team Member spawning in tests/test_brainstorm_integration.py
  - Test all 4 core roles spawn successfully
  - Test all 5 roles spawn with --with-security flag
  - Test member count matches expected
- [ ] T011 [US1] Add integration tests for proposal collection in tests/test_brainstorm_integration.py
  - Test all proposals collected within timeout
  - Test proposals aggregated by role
  - Test partial collection handles gracefully

### User Story 1 - Implementation AFTER Tests

- [ ] T012 [US1] Implement Team Member spawning via Agent tool
  - Use Agent tool with `team_name` and `name` parameters
  - Spawn member-{role-id} naming convention
  - Track spawned members in runtime state
- [ ] T013 [US1] Implement proposal request message (`propose` type)
  - Define message structure with role, context, instructions
  - Send to each role member via SendMessage
- [ ] T014 [US1] Implement proposal response handling (`proposal` type)
  - Parse structured proposal from each role
  - Store proposals in memory for later merge
- [ ] T015 [US1] Implement proposal collection phase
  - Wait for all role proposals to arrive
  - Aggregate proposals by role
  - Handle timeout gracefully

**Checkpoint**: User Story 1 complete and tested - roles can generate proposals

---

## Phase 4: User Story 2 - Devil's Advocate Challenge (Priority: P2)

**Goal**: Enable devil's advocate to challenge assumptions and expose flaws

**Independent Test**: Introduce a flawed assumption and verify devil's advocate challenges it

### User Story 2 - Tests FIRST (TDD)

- [ ] T016 [US2] Add unit tests for devil's advocate challenge generation in tests/test_brainstorm_us2.py
  - Test challenge rate (at least 3 challenges per major assumption)
  - Test "what could go wrong" questioning pattern
  - Test edge case probing
- [ ] T017 [US2] Add unit tests for counter-argument routing in tests/test_brainstorm_us2.py
  - Test counter_argument message structure
  - Test routing to correct target role
  - Test contested vs unanimous tracking
- [ ] T018 [US2] Add unit tests for debate phase initialization in tests/test_brainstorm_us2.py
  - Test devil's advocate spawn timing (debate phase only)
  - Test proposal context sharing
  - Test debate initiation message format
- [ ] T019 [US2] Add integration tests for devil's advocate challenges in tests/test_brainstorm_integration.py
  - Test flawed assumption triggers challenge
  - Test challenge response cycle
  - Test escalation when consensus fails
- [ ] T020 [US2] Add E2E test for devil's advocate scenario in tests/test_brainstorm_e2e.py
  - Test: Architect proposes unjustified microservices → devil's advocate challenges
  - Verify: Challenge includes complexity trade-offs question
  - Verify: Architect responds or escalates

### User Story 2 - Implementation AFTER Tests

- [ ] T021 [US2] Spawn Devil's Advocate member (member-devil) for debate phase
  - Spawn only when debate phase starts
  - Provide proposal context to devil's advocate
- [ ] T022 [US2] Implement debate initiation message (`debate` type)
  - Notify all members debate phase has started
  - Share all proposals with devil's advocate
- [ ] T023 [US2] Implement counter-argument handling (`counter_argument` type)
  - Parse challenges from devil's advocate
  - Route challenges to relevant role
  - Track contested vs unanimous points
- [ ] T024 [US2] Implement devil's advocate challenge generation
  - Challenge every assumption stated as fact
  - Ask "what could go wrong?" for each point
  - Probe edge cases and boundary conditions

**Checkpoint**: User Story 2 complete and tested - devil's advocate actively challenges

---

## Phase 5: User Story 3 - Structured Decision Making (Priority: P3)

**Goal**: Present multiple options with trade-offs for contested points, user makes final decision

**Independent Test**: Introduce a contested point and verify options with pros/cons are presented

### User Story 3 - Tests FIRST (TDD)

- [ ] T025 [US3] Add unit tests for options generation in tests/test_brainstorm_us3.py
  - Test multiple options generation when consensus fails
  - Test pros/cons documentation for each option
  - Test risk assessment inclusion
- [ ] T026 [US3] Add unit tests for decision request/response in tests/test_brainstorm_us3.py
  - Test decision_request message structure
  - Test decision message parsing
  - Test decision recording with rationale
- [ ] T027 [US3] Add unit tests for decision recording in tests/test_brainstorm_us3.py
  - Test Decisions Log format
  - Test decision persistence
  - Test decision validation
- [ ] T028 [US3] Add integration tests for decision flow in tests/test_brainstorm_integration.py
  - Test contested point triggers options generation
  - Test user decision updates spec
  - Test unanimous case (EC-003) skips decision flow
- [ ] T029 [US3] Add E2E test for decision scenario in tests/test_brainstorm_e2e.py
  - Test: Two roles disagree on architecture → options with pros/cons presented
  - Verify: User selects option → decision recorded in spec
  - Verify: Appendix reflects decision rationale

### User Story 3 - Implementation AFTER Tests

- [ ] T030 [US3] Implement options generation when consensus fails
  - When roles disagree, collect multiple options
  - Document pros and cons for each option
  - Include risk assessment
- [ ] T031 [US3] Implement decision request to user (`decision_request` type)
  - Present contested topic clearly
  - Show all options with trade-offs
  - Request user selection
- [ ] T032 [US3] Implement user decision recording (`decision` type)
  - Accept user decision via message
  - Record decision with rationale
  - Update spec with Decisions Log
- [ ] T033 [US3] Handle unanimous agreement case (EC-003)
  - Skip decision flow if all points are agreed
  - Proceed directly to spec generation

**Checkpoint**: User Story 3 complete and tested - user can make decisions

---

## Phase 6: User Story 4 - Complete Debate Record (Priority: P4)

**Goal**: Preserve full debate transcript as appendix for future reference

**Independent Test**: Generate spec and verify appendix contains complete transcript

### User Story 4 - Tests FIRST (TDD)

- [ ] T034 [US4] Add unit tests for spec.md generation in tests/test_brainstorm_us4.py
  - Test spec sections populated from role proposals
  - Test user decisions applied to contested points
  - Test spec completeness per SC-006 checklist
- [ ] T035 [US4] Add unit tests for transcript collection in tests/test_brainstorm_us4.py
  - Test chronological message storage
  - Test message type inclusion
  - Test no messages omitted verification
- [ ] T036 [US4] Add unit tests for appendix generation in tests/test_brainstorm_us4.py
  - Test appendix file naming (brainstorm-appendix.md)
  - Test chronological format
  - Test completeness verification
- [ ] T037 [US4] Add integration tests for output generation in tests/test_brainstorm_integration.py
  - Test spec.md generated with all sections
  - Test appendix.md generated with full transcript
  - Test file format correctness
- [ ] T038 [US4] Add E2E test for complete flow in tests/test_brainstorm_e2e.py
  - Test: Full brainstorm session → spec.md + appendix.md
  - Verify: Appendix contains all proposals, challenges, decisions
  - Verify: SC-005 no messages omitted

### User Story 4 - Implementation AFTER Tests

- [ ] T039 [US4] Implement spec.md generation from proposals and decisions
  - Merge all role proposals into spec sections
  - Apply user decisions to contested points
  - Generate complete spec.md output
- [ ] T040 [US4] Implement debate transcript collection
  - Store all messages chronologically in memory
  - Include proposals, challenges, responses, decisions
- [ ] T041 [US4] Implement appendix generation
  - Generate brainstorm-appendix.md from transcript
  - Format as chronological record
  - Ensure no messages omitted (SC-005)

**Checkpoint**: User Story 4 complete and tested - spec and appendix generated

---

## Phase 7: Polish & Edge Cases

**Purpose**: Handle edge cases and finalize

### Edge Cases - Tests FIRST

- [ ] T042 [P] Add unit tests for EC-001 (lite mode fallback) in tests/test_brainstorm_edge.py
  - Test team mode unavailable detection
  - Test warning message display
  - Test lite mode sequential prompts
- [ ] T043 [P] Add unit tests for EC-002 (vague idea) in tests/test_brainstorm_edge.py
  - Test empty idea detection
  - Test vague idea detection
  - Test clarification prompt
- [ ] T044 [P] Add unit tests for EC-004 (mid-session security expert) in tests/test_brainstorm_edge.py
  - Test security concern detection
  - Test mid-session expert invitation
  - Test graceful role addition
- [ ] T045 [P] Add unit tests for EC-005 (debate intervention) in tests/test_brainstorm_edge.py
  - Test unproductive debate detection
  - Test user intervention trigger
  - Test immediate decision acceptance

### Edge Cases - Implementation AFTER Tests

- [ ] T046 Implement EC-002: Empty/vague idea handling
  - Detect vague or empty idea input
  - Prompt user for clarification before proceeding
- [ ] T047 Implement EC-004: Mid-session security expert invitation
  - Allow inviting security expert during debate
  - Handle mid-session role addition gracefully
- [ ] T048 Implement EC-005: Debate intervention
  - Allow user to intervene when debate is unproductive
  - Accept immediate decisions from user

### Final Polish

- [ ] T049 [P] Run full test suite and verify all tests pass
- [ ] T050 [P] Verify SC-006 completeness score ≥ 80%
- [ ] T051 [P] Update REVIEWERS.md with review checklist
- [ ] T052 [P] Final documentation review

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - Each story: Tests BEFORE Implementation (TDD)
  - Stories can proceed in parallel if resources allow
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Execution (TDD Flow)

```
For each user story (US1 → US2 → US3 → US4):
    1. Complete all test tasks (T0xx)
    2. Verify tests fail (RED)
    3. Complete all implementation tasks (T0xx)
    4. Verify tests pass (GREEN)
    5. Refactor if needed
    6. Move to next story
```

### Parallel Opportunities

Within each user story phase:
- Test tasks can run in parallel (different test files/functions)
- Implementation tasks can run in parallel (different functions)

Between user stories:
- US1 must complete before US4 (US4 needs proposals)
- US2 and US3 can run in parallel (independent)
- Polish tasks T042-T045 can run in parallel

---

## Test File Structure

```
tests/
├── test_brainstorm_us1.py          # US1 unit tests
├── test_brainstorm_us2.py          # US2 unit tests
├── test_brainstorm_us3.py          # US3 unit tests
├── test_brainstorm_us4.py          # US4 unit tests
├── test_brainstorm_integration.py  # Integration tests
├── test_brainstorm_e2e.py         # E2E tests
└── test_brainstorm_edge.py         # Edge case tests
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete US1 Tests (T007-T011)
4. Complete US1 Implementation (T012-T015)
5. **STOP and VALIDATE**: Test proposal generation works
6. Deploy/demo if ready

### Full TDD Flow

1. Complete Phase 1-2
2. For US1: Tests → Implement → Verify
3. For US2: Tests → Implement → Verify
4. For US3: Tests → Implement → Verify
5. For US4: Tests → Implement → Verify
6. Polish: Edge case tests → Implement → Verify
7. Final validation

---

## Success Criteria Validation

| SC | Description | Verification Method |
|-----|-------------|---------------------|
| SC-001 | Proposal generation < 5 min | Integration test timer |
| SC-002 | Devil's advocate ≥ 3 challenges | Unit test assertion |
| SC-003 | Debate resolution ≤ 2 rounds | Integration test |
| SC-004 | spec.md completeness | Unit test checklist |
| SC-005 | Appendix no omissions | Unit test count |
| SC-006 | Completeness score ≥ 80% | Automated checklist |

---

## Notes

- Tests are MANDATORY for this feature - TDD approach required
- All test tasks must pass before implementation tasks for same story
- Integration tests use mocked Team mode
- E2E tests require actual Team mode environment
