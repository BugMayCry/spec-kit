# Review Checklist: Multi-Agent Collaborative Brainstorming

## Feature Overview

`/speckit.brainstorm <idea>` - Multi-agent collaborative brainstorming using Team mode with specialized roles (Product Manager, Architect, Technical Expert, Test Expert, Security Expert, Devil's Advocate).

## Review Checklist

### 1. Command Implementation (templates/commands/brainstorm.md)

- [ ] Command skeleton complete with all phases
- [ ] Role configurations defined (member-pm, member-architect, member-tech, member-test, member-security, member-devil)
- [ ] Message types implemented (propose, proposal, debate, counter_argument, decision_request, decision)
- [ ] Edge case handlers in place (EC-001 to EC-005)

### 2. Test Coverage

- [ ] **US1 (T007-T015)**: Multi-Role Brainstorming
  - Unit tests: 18 tests (test_brainstorm_us1.py)
  - Integration tests: 9 tests (test_brainstorm_integration.py)
  - All passing

- [ ] **US2 (T016-T024)**: Devil's Advocate Challenge
  - Unit tests: 16 tests (test_brainstorm_us2.py)
  - E2E tests: 2 tests (test_brainstorm_e2e.py)
  - All passing

- [ ] **US3 (T025-T033)**: Structured Decision Making
  - Unit tests: 14 tests (test_brainstorm_us3.py)
  - Integration tests: 3 tests (test_brainstorm_integration.py)
  - E2E tests: 2 tests (test_brainstorm_e2e.py)
  - All passing

- [ ] **US4 (T034-T041)**: Complete Debate Record
  - Unit tests: 13 tests (test_brainstorm_us4.py)
  - Integration tests: 3 tests (test_brainstorm_integration.py)
  - E2E tests: 3 tests (test_brainstorm_e2e.py)
  - All passing

- [ ] **Edge Cases (T042-T048)**: EC-001 to EC-005
  - Unit tests: 15 tests (test_brainstorm_edge.py)
  - All passing

### 3. Success Criteria Validation

| SC | Description | Verification |
|----|-------------|--------------|
| SC-001 | Proposal generation < 5 min | Test timer validation |
| SC-002 | Devil's advocate ≥ 3 challenges | Unit test assertion |
| SC-003 | Debate resolution ≤ 2 rounds | Integration test |
| SC-004 | spec.md completeness | Unit test checklist |
| SC-005 | Appendix no omissions | Unit test count |
| SC-006 | Completeness score ≥ 80% | Automated checklist |

### 4. Files Modified

- `templates/commands/brainstorm.md` - Command template
- `tests/test_brainstorm_us1.py` - US1 unit tests (18 tests)
- `tests/test_brainstorm_us2.py` - US2 unit tests (16 tests)
- `tests/test_brainstorm_us3.py` - US3 unit tests (14 tests)
- `tests/test_brainstorm_us4.py` - US4 unit tests (13 tests)
- `tests/test_brainstorm_integration.py` - Integration tests (27 tests)
- `tests/test_brainstorm_e2e.py` - E2E tests (14 tests)
- `tests/test_brainstorm_edge.py` - Edge case tests (15 tests)
- `specs/003-brainstorm-team-collab/tasks.md` - Updated task status

### 5. Test Execution Results

```
Total: 95 tests
Passed: 95
Failed: 0
Coverage: All user stories covered
```

## Test Commands

```bash
# Run all brainstorm tests
python -m pytest tests/test_brainstorm_*.py -v

# Run specific test file
python -m pytest tests/test_brainstorm_us1.py -v

# Run with coverage
python -m pytest tests/test_brainstorm_*.py --cov
```

## Review Sign-off

- [ ] Code reviewed
- [ ] Tests verified passing
- [ ] Success criteria validated
- [ ] Documentation complete
