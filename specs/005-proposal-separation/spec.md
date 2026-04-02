# Feature Specification: Split Brainstorm Output into Proposal Files

**Feature Branch**: `005-proposal-separation`
**Created**: 2026-04-02
**Status**: Spec
**Input**: "brainstorm命令头脑风暴的结果区分用户故事和技术实现，用户故事写入spec.prolosal.md，技术方案写入plan.prolosal.md。执行specify命令从spec.prolosal.md进行细化，在执行plan命令时，需要增加结合plan.prolosal.md做分析"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 产物分离 (Priority: P1)

PM 希望能独立审阅和迭代 brainstorm 产出的用户故事，无需过滤技术细节。

**Why this priority**: 这是本次改进的核心价值主张 - 清晰的职责分离

**Independent Test**: Can be fully tested by executing brainstorm and verifying two files exist with correct content types

**Acceptance Scenarios**:

1. **Given** brainstorm 命令执行完成，**When** 查看输出目录，**Then** 存在 `spec.proposal.md` 和 `plan.proposal.md` 两个文件
2. **Given** `spec.proposal.md` 存在，**When** 打开文件查看内容，**Then** 只包含用户故事、验收标准等业务内容，不包含任何技术实现细节
3. **Given** `plan.proposal.md` 存在，**When** 打开文件查看内容，**Then** 只包含技术方案、架构设计等内容，不包含业务需求细节

---

### User Story 2 - specify 无缝衔接 (Priority: P2)

PM 希望 specify 命令能直接基于 `spec.proposal.md` 细化，无需手动提取内容。

**Why this priority**: 减少手动操作，提高迭代效率

**Independent Test**: Can be fully tested by running specify command and verifying it reads from spec.proposal.md

**Acceptance Scenarios**:

1. **Given** `spec.proposal.md` 存在，**When** 执行 specify 命令，**Then** 系统自动读取 `spec.proposal.md` 作为输入
2. **Given** specify 命令执行完成，**Then** 产出细化的 `spec.md`，内容基于原始用户故事扩展

---

### User Story 3 - plan 综合分析 (Priority: P3)

技术负责人希望 plan 命令能结合 `plan.proposal.md` 和 `spec.md` 做技术分析，确保决策锚定用户需求。

**Why this priority**: 技术方案应服务于业务需求，保持双向可追溯性

**Independent Test**: Can be fully tested by running plan command and verifying it references plan.proposal.md content

**Acceptance Scenarios**:

1. **Given** `plan.proposal.md` 存在，**When** 执行 plan 命令，**Then** 系统加载该文件获取技术背景
2. **Given** plan 命令执行完成，**Then** 技术决策能体现对用户需求的追溯

---

### Edge Cases

- 如果 `spec.proposal.md` 不存在但 `spec.md` 存在：specify 应回退到读取 `spec.md`（向后兼容）
- 如果 `plan.proposal.md` 不存在：plan 命令应提示用户先生成该文件，不执行 plan
- 如果两个文件都存在但内容为空：应提示内容无效

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: brainstorm Phase 4 必须同时生成 `spec.proposal.md` 和 `plan.proposal.md` 两个文件
- **FR-002**: `spec.proposal.md` 必须只包含用户故事内容（来自 PM + Test 角色），不得包含技术实现细节
- **FR-003**: `plan.proposal.md` 必须只包含技术方案内容（来自 Architect + Tech 角色），不得包含业务需求细节
- **FR-004**: specify 命令必须优先读取 `spec.proposal.md`，当其不存在时回退到 `spec.md`
- **FR-005**: plan 命令必须读取 `plan.proposal.md` 并结合 `spec.md` 中的用户需求做技术分析
- **FR-006**: 所有提案文件与最终文档保持在同一 spec 目录下

### Key Entities

- **Proposal File**: brainstorm 产出的中间文档，作为 specify 和 plan 的输入
- **spec.proposal.md**: 用户故事提案文件，描述用户需求和验收标准
- **plan.proposal.md**: 技术方案提案文件，描述架构设计和实现考虑

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: brainstorm 完成后生成的两个提案文件都存在且内容非空（每个文件 > 50 字节）
- **SC-002**: `spec.proposal.md` 中不包含任何技术实现细节（无框架名称、无 API 设计、无数据结构定义）
- **SC-003**: specify 命令能成功从 `spec.proposal.md` 读取并生成细化的 `spec.md`
- **SC-004**: plan 命令能成功从 `plan.proposal.md` 读取并生成技术分析
- **SC-005**: 现有 `spec.md` 格式继续兼容（向后兼容）

## Clarifications

### Session 2026-04-02

- Q: spec.proposal.md 和 plan.proposal.md 的内容结构是否需要明确定义？ → A: 定义标准化章节结构（参考 spec.md 和 plan.md），同时允许角色自行补充内容
- Q: 向后兼容的具体机制是什么？ → A: fallback 机制 - specify 优先读取 spec.proposal.md，不存在时回退到 spec.md
- Q: plan 命令如果没有找到 plan.proposal.md，应该如何处理？ → A: 提示用户先生成 plan.proposal.md，不执行 plan

## Assumptions

- 团队成员理解新的文件结构和产出约定
- 用户愿意在迭代过程中保持两个提案文件的同步更新
- 向后兼容的 fallback 机制在过渡期发挥作用

## Proposal File Structures

### spec.proposal.md 章节结构

基于 spec.md 的用户导向章节（**必须包含**，可补充）：

1. **User Scenarios** - 用户场景和用户故事
2. **Requirements** - 功能性需求（不含技术细节）
3. **Success Criteria** - 成功标准（可测量）
4. **Edge Cases** - 边界情况和异常处理

*角色可自行补充：PM 可增加业务背景、优先级；Test 可增加验收标准细节*

### plan.proposal.md 章节结构

基于 plan.md 的技术导向章节（**必须包含**，可补充）：

1. **Technical Decisions** - 技术决策点
2. **System Design** - 系统设计
3. **Risks & Mitigations** - 风险与缓解措施
4. **Implementation Approach** - 实现路径

*角色可自行补充：Architect 可增加架构图；Tech 可增加技术选型理由*

---
*Proposal 文件由 brainstorm 阶段生成，供 specify 和 plan 命令使用*
