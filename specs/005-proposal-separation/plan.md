# Implementation Plan: Split Brainstorm Output

**Branch**: `005-proposal-separation` | **Date**: 2026-04-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-proposal-separation/spec.md`

## Summary

本次改进将 brainstorm 命令的输出从单一 `spec.md` 拆分为两个提案文件：
- `spec.proposal.md` - 用户故事（PM + Test 角色产出）
- `plan.proposal.md` - 技术方案（Architect + Tech 角色产出）

specify 命令从 `spec.proposal.md` 细化，plan 命令结合 `plan.proposal.md` 分析。

## Technical Context

**Language/Version**: Markdown + Bash/PowerShell
**Primary Dependencies**: 无新增依赖（纯工作流变更）
**Storage**: N/A（无数据存储）
**Testing**: 手动测试 + E2E 测试（命令执行验证）
**Target Platform**: Claude Code CLI 工作流工具
**Project Type**: CLI Workflow / Process Improvement
**Performance Goals**: N/A
**Constraints**: 保持向后兼容
**Scale/Scope**: 3 个命令模板文件修改

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**状态**: ✅ 无约束违反
- Constitution 为空模板，无特定约束
- 本次改进为工作流变更，不涉及代码实现

## Project Structure

### Documentation (this feature)

```text
specs/005-proposal-separation/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - 纯工作流变更)
├── data-model.md        # Phase 1 output (N/A - 无数据模型)
├── quickstart.md        # Phase 1 output (N/A - 无需安装)
├── contracts/           # Phase 1 output (N/A - 无外部接口)
└── tasks.md             # Phase 2 output (from /speckit.tasks)
```

### Source Code (templates/commands)

```text
templates/commands/
├── brainstorm.md        # 修改 Phase 4 Output
├── specify.md          # 修改文件读取逻辑
└── plan.md             # 增加 plan.proposal.md 加载
```

**Structure Decision**:
- 仅修改 3 个命令模板文件
- brainstorm.md: 修改输出格式
- specify.md: 增加 spec.proposal.md 读取
- plan.md: 增加 plan.proposal.md 加载

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 无 | N/A | N/A |

## Implementation Details

### 1. brainstorm.md 修改

**位置**: `templates/commands/brainstorm.md`

**Phase 4 Output 部分修改**:

原内容:
```markdown
- Generate `specs/<number>-<short-name>/spec.md` (concise draft for specify)
  - **IMPORTANT**: Replace `$STATUS` in the generated spec with `Proposal`
  - Filename format: `proposal-<number>-<short-name>-spec.md` (note: "proposal-" prefix)
```

修改为:
```markdown
- Generate `specs/<number>-<short-name>/spec.proposal.md` (user stories draft)
  - **Source**: PM + Test Expert contributions
  - **Contains**: User scenarios, user stories, acceptance criteria, priority
  - **No technical details**
- Generate `specs/<number>-<short-name>/plan.proposal.md` (technical proposal draft)
  - **Source**: Architect + Tech Expert contributions
  - **Contains**: System design, tech stack, risks, integration points
- Generate `specs/<number>-<short-name>/brainstorm-appendix.md` (full transcript, unchanged)
```

**Output Format 部分修改**:

原内容:
```markdown
### spec.md (Concise Draft for Specify)
A clean, concise spec that specify can understand and refine...
```

修改为:
```markdown
### spec.proposal.md (User Stories Draft)
User stories and requirements extracted from brainstorming. This is what specify refines into final spec.
- User needs and pain points (from PM)
- User scenarios and journeys (from PM, reviewed by Test)
- User stories with priorities
- Acceptance criteria (from Test)
- Business value and ROI considerations

### plan.proposal.md (Technical Proposal Draft)
Technical architecture and implementation considerations extracted from brainstorming. This is what plan analyzes and expands.
- System design proposals (from Architect)
- Technology selection options (from Tech Expert)
- Scalability and reliability considerations (from Architect)
- Implementation risks and constraints (from Tech Expert)
- Integration points and dependencies
- Non-functional requirements (DFX)

### Appendix: brainstorm-appendix.md (unchanged)
- Full debate transcript
```

### 2. specify.md 修改

**位置**: `templates/commands/specify.md`

**Step 2e 部分修改**:

原内容:
```markdown
e. **Handle existing brainstorm directory**:
   - If directory found with matching short-name AND contains `brainstorm-appendix.md`:
     1. Inform user: "Found existing brainstorm session: specs/<existing-dir>/"
     2. Present options:
        - **Continue (C)**: Use existing directory - recommended if brainstorm was just completed
        - **New (N)**: Create new directory with next available number
     3. If user chooses **Continue**:
        - Run: `git checkout -b <existing-dir> && export SPECIFY_FEATURE=<existing-dir>`
        - Load `specs/<existing-dir>/spec.md` as the starting draft
        - Load `specs/<existing-dir>/brainstorm-appendix.md` for technical context
        - Skip to step 4 to refine the existing spec
```

修改为:
```markdown
e. **Handle existing brainstorm directory**:
   - If directory found with matching short-name AND contains `spec.proposal.md`:
     1. Inform user: "Found existing brainstorm session: specs/<existing-dir>/"
     2. Present options:
        - **Continue (C)**: Use existing directory - recommended if brainstorm was just completed
        - **New (N)**: Create new directory with next available number
     3. If user chooses **Continue**:
        - Run: `git checkout -b <existing-dir> && export SPECIFY_FEATURE=<existing-dir>`
        - Load `specs/<existing-dir>/spec.proposal.md` as the starting draft (user stories from brainstorm)
        - Load `specs/<existing-dir>/brainstorm-appendix.md` for additional context
        - Skip to step 4 to refine the spec proposal into final spec
```

### 3. plan.md 修改

**位置**: `templates/commands/plan.md`

**Step 2 部分修改**:

原内容:
```markdown
2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).
```

修改为:
```markdown
2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).

   **Additionally, check for and load plan.proposal.md**:
   - If `plan.proposal.md` exists in the feature directory (from brainstorm), load it
   - This file contains technical proposals from Architect and Tech Expert extracted during brainstorm
   - Integrate its contents into the Technical Context analysis phase
   - Extract technology choices, integration points, and technical constraints from plan.proposal.md
```

**Phase 0 部分修改**:

原内容:
```markdown
### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task
```

修改为:
```markdown
### Phase 0: Outline & Research

**Prerequisite**: Ensure plan.proposal.md has been loaded (from Step 2)

1. **Analyze plan.proposal.md** (if exists):
   - Extract technology choices proposed by Tech Expert
   - Extract system design proposals from Architect
   - Extract integration points and dependencies
   - Extract technical constraints and risks
   - Mark any unvalidated proposals as "NEEDS VERIFICATION"

2. **Extract unknowns from Technical Context** above (including plan.proposal analysis):
   - For each NEEDS CLARIFICATION → research task
   - For each NEEDS VERIFICATION (from plan.proposal) → validation task
   - For each dependency → best practices task
   - For each integration → patterns task
```

## Backward Compatibility

specify 命令 fallback 行为：
- 优先读取 `spec.proposal.md`
- 如果不存在，回退到 `spec.md`

plan 命令：
- 需要 `plan.proposal.md` 存在
- 如果不存在，提示用户先生成

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 用户不理解新的文件结构 | Medium | Medium | 更新文档，提供示例 |
| 旧项目迁移成本 | Low | Low | 提供迁移指南，保持 fallback |
| 指定角色边界模糊 | Medium | Low | 明确模板章节定义 |

## Testing Approach

### E2E 测试场景

1. **brainstorm 生成双文件**
   ```
   执行 brainstorm
   验证 spec.proposal.md 存在且包含用户故事章节
   验证 plan.proposal.md 存在且包含技术方案章节
   ```

2. **specify 从 spec.proposal.md 细化**
   ```
   指定 spec.proposal.md 存在
   执行 specify
   验证读取了 spec.proposal.md
   验证生成了 spec.md
   ```

3. **plan 结合 plan.proposal.md 分析**
   ```
   指定 plan.proposal.md 存在
   执行 plan
   验证读取了 plan.proposal.md
   验证技术决策引用了提案内容
   ```

4. **向后兼容 - specify fallback**
   ```
   只存在 spec.md（无 spec.proposal.md）
   执行 specify
   验证 fallback 到 spec.md
   ```

## Files to Modify

| File | Change Type | Lines Affected |
|------|-------------|----------------|
| `templates/commands/brainstorm.md` | Output Format | ~20 lines |
| `templates/commands/specify.md` | File Detection | ~10 lines |
| `templates/commands/plan.md` | Context Loading | ~15 lines |
