# Implementation Plan: Brainstorm命令仓库认知增强

**Branch**: `004-brainstorm-repo-awareness` | **Date**: 2026-04-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-brainstorm-repo-awareness/spec.md`

## Summary

增强 brainstorm 命令，在提案准备前增加仓库认知阶段。架构师和技术专家必须先了解项目仓库的架构和技术细节后才能开始准备提案。同时，brainstorm 生成的 spec.md 文件需采用双重标识（文件名+Status字段）标记为"提案"。

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, httpx, json5
**Storage**: N/A (文件模板系统)
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Linux/macOS/Windows)
**Project Type**: CLI tool / Template management system
**Performance Goals**: 仓库信息提取 < 2秒
**Constraints**: 保持向后兼容，不破坏现有brainstorm流程
**Scale/Scope**: 单项目维度，不涉及多用户

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| 单一职责 | PASS | brainstorm命令仍负责提案生成 |
| 最小化变更 | PASS | 仅修改brainstorm.md模板 |
| 向后兼容 | PASS | 添加可选的认知阶段 |

## Project Structure

### Documentation (this feature)

```text
specs/004-brainstorm-repo-awareness/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
templates/commands/
├── brainstorm.md       # [MODIFY] Add repository awareness phase
└── [... other commands]

templates/spec-template.md  # [MODIFY] Add Proposal status support
```

**Structure Decision**: 修改现有模板文件，不添加新文件结构

## Complexity Tracking

> No violations to justify

## Implementation Details

### Phase 0: Research Required

1. **仓库信息提取**:
   - 研究如何从项目中提取：README内容、架构文档路径、技术栈配置
   - 确定信息源优先级

2. **模板修改方案**:
   - 在brainstorm.md中插入仓库认知阶段
   - 定义用户交互流程

3. **提案标识方案**:
   - 确定文件名格式（proposal-{number}-{short-name}-spec.md）
   - 确定Status字段值（Proposal）

### Phase 1: Design

#### Data Model

| Entity | Attributes | Purpose |
|--------|------------|---------|
| 认知确认记录 | userId, timestamp, skipUsed, modeSelected | 跟踪用户完成状态 |
| 仓库概览 | architecture, techStack, dirStructure, docPaths | 展示给用户的信息 |

#### Interface Contracts

**Brainstorm命令新增参数**:
```
--mode {full|quick}  # 完整模式/快速模式
--skip-awareness      # 跳过认知阶段（已确认用户）
```

**Spec文件命名**:
```
proposal-{number}-{short-name}-spec.md
```

### Phase 2: Implementation Tasks

1. 修改 `templates/commands/brainstorm.md` - 添加认知阶段
2. 修改 `templates/spec-template.md` - 支持Proposal状态
3. 添加测试用例
4. 更新文档
