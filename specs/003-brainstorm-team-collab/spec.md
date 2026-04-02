# Feature Specification: Multi-Agent Collaborative Brainstorming

**Feature Branch**: `003-brainstorm-team-collab`
**Created**: 2026-04-02
**Status**: Draft
**Input**: Enable multi-agent collaborative specification writing using Claude Code Team mode, where specialized roles work together with a devil's advocate to produce high-quality specs

---

## Clarifications

### Session 2026-04-02

- Q: 辩论过程中产生的消息内容存储在哪里？ → A: 仅保存在运行时内存中，附录在会话结束时生成文件
- Q: EC-001 中 "lite mode" 的具体行为是什么？ → A: 顺序调用各角色视角，每次只有一个角色思考然后合并，不进行实时辩论
- Q: SC-006 主观满意度如何客观验证？ → A: 替换为自动完整性检查：spec 完整性得分 ≥ 80%（检查清单覆盖情况），用户满意度降级为设计目标不作为验收条件

---

## User Scenarios & Testing

### User Story 1 - Multi-Role Brainstorming (Priority: P1)

As a product owner, I want multiple specialized agents to collaboratively develop a specification so that I can get diverse perspectives and higher quality output than single-agent writing.

**Why this priority**: This is the core value proposition - enabling collaborative spec development.

**Independent Test**: Can be tested by running `/speckit.brainstorm <idea>` and verifying that multiple role proposals are generated and merged into a coherent spec.

**Acceptance Scenarios**:

1. **Given** Team mode is enabled, **When** I run `/speckit.brainstorm Build a payment system`, **Then** each role (PM, Architect, Technical Expert, Test Expert) generates their proposal independently.

2. **Given** Team mode is enabled with `--with-security`, **When** I run the brainstorm command, **Then** the Security Compliance Expert also participates and provides their perspective.

3. **Given** the debate phase is active, **When** there are contested points, **Then** each role provides multiple options with pros and cons for my decision.

---

### User Story 2 - Devil's Advocate Challenge (Priority: P2)

As a product owner, I want a dedicated devil's advocate agent to challenge every assumption so that I can identify and address potential flaws before implementation.

**Why this priority**: The devil's advocate is the key differentiator that prevents groupthink and weak assumptions from being accepted.

**Independent Test**: Can be tested by introducing a flawed assumption and verifying the devil's advocate identifies and challenges it.

**Acceptance Scenarios**:

1. **Given** the debate phase is active, **When** the Architect proposes a microservices architecture without justification, **Then** the devil's advocate challenges the assumption and asks about complexity trade-offs.

2. **Given** the devil's advocate has challenged a point, **When** the relevant role responds, **Then** the debate continues until either consensus is reached or a decision is escalated.

---

### User Story 3 - Structured Decision Making (Priority: P3)

As a product owner, I want to see multiple options with trade-offs for contested points so that I can make informed decisions based on business priorities.

**Why this priority**: Ensures the product owner (user) has the final say with complete information.

**Independent Test**: Can be tested by introducing a contested architectural decision and verifying that multiple options with pros/cons are presented.

**Acceptance Scenarios**:

1. **Given** two roles disagree on a technical approach, **When** consensus cannot be reached, **Then** both options are documented with pros, cons, and risk assessment for my decision.

2. **Given** I have made a decision on a contested point, **When** the decision is recorded, **Then** it is added to the Decisions Log section of the spec.

---

### User Story 4 - Complete Debate Record (Priority: P4)

As a product owner, I want the full debate transcript preserved as an appendix so that I can trace the reasoning behind decisions later.

**Why this priority**: Maintains institutional knowledge and enables future team members to understand why certain decisions were made.

**Independent Test**: Can be tested by generating a spec and verifying the appendix contains the complete debate transcript.

**Acceptance Scenarios**:

1. **Given** a brainstorm session has completed, **When** the spec.md is generated, **Then** a corresponding `brainstorm-appendix.md` is created with the full transcript.

2. **Given** I want to review the debate, **When** I open the appendix, **Then** I can see all proposals, counter-arguments, and decisions in chronological order.

---

### Edge Cases

- **EC-001**: Team mode not enabled → Display warning, offer to run in single-agent "lite" mode
- **EC-002**: User provides vague/empty idea → Prompt for clarification before proceeding
- **EC-003**: All roles reach unanimous agreement → Skip debate phase, proceed directly to spec generation
- **EC-004**: Security expert not included but security concerns arise during debate → Option to invite security expert mid-session
- **EC-005**: Debate becomes circular or unproductive → Team Lead (user) can intervene and make immediate decision

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST support `/speckit.brainstorm <idea>` command with optional `--with-security` flag

- **FR-002**: System MUST spawn Team Members for each role: PM, Architect, Technical Expert, Test Expert (and Security Expert if flagged)

- **FR-003**: System MUST collect independent proposals from each role before initiating debate

- **FR-004**: System MUST initiate debate phase with devil's advocate participating via Team SendMessage

- **FR-005**: System MUST track contested vs unanimous points during debate

- **FR-006**: System MUST present multiple options with pros/cons when roles disagree

- **FR-007**: System MUST allow user to make final decisions on contested points

- **FR-008**: System MUST generate spec.md with contributions from all roles

- **FR-009**: System MUST preserve full debate transcript as appendix

- **FR-010**: System MUST fallback to single-agent mode when Team mode is unavailable with appropriate warning

### Key Entities

- **Proposal**: Structured output from each role containing their analysis, key points, risks, and questions

- **Decision**: Final choice made by Product Owner on contested points, including rationale

- **DebateRecord**: Chronological transcript of all messages exchanged during debate phase

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: All core roles (PM, Architect, Technical Expert, Test Expert) successfully generate proposals within 5 minutes of starting

- **SC-002**: Devil's advocate raises at least 3 challenges per major assumption in proposals

- **SC-003**: Contested points are resolved with documented options and pros/cons within 2 rounds of debate

- **SC-004**: Generated spec.md contains all sections from spec-template.md with content from respective role perspectives

- **SC-005**: Appendix accurately reflects the complete debate with no messages omitted

- **SC-006**: Spec completeness score ≥ 80% (verified by automated checklist: User Story ≥ 2, each with acceptance scenarios; Edge Cases exists; Functional requirements ≥ 5; Success Criteria all quantifiable; Assumptions documented)

**Design Goal (not a pass/fail criterion)**: User satisfaction rating of 4/5 or higher for spec quality compared to single-agent output

---

## Assumptions

- **A1**: Claude Code Team mode is enabled in the environment (via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)

- **A2**: User has basic understanding of spec-driven development workflow

- **A3**: The feature is designed for medium-to-large features where multi-perspective review adds value; trivial features may not benefit

- **A4**: Debate phase typically takes 10-30 minutes depending on feature complexity and number of contested points

- **A5**: User is willing to actively participate as Product Owner during decision phase

- **A6**: Roles use their specialized knowledge effectively without requiring extensive context setup
