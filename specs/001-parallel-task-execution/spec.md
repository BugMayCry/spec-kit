# SPEC.md: Parallel Task Execution for Spec-Driven Development

**Feature**: Parallel Task Execution for Spec-Driven Development
**Version**: 1.0
**Status**: Draft
**Feature Branch**: `001-parallel-task-execution`
**Created**: 2026-04-01
**Input**: 用户同意的架构决策

---

## 1. 概述

### 1. 1 动机

当前 `/speckit.implement` 以串行方式执行任务。对于包含多个独立用户故事（US1, US2, US3）的特性，这浪费了并行处理机会。

### 1. 2 目标

扩展 `/speckit.implement` 支持自动并行执行多个用户故事，缩短实现时间，同时保持 SDD 的质量和可追溯性。

### 1. 3 范围

- 修改 `/speckit.implement` 命令，增加并行检测和执行能力
- 利用 Claude Code Team 模式实现多 Agent 协作
- 不新增独立命令，保持 4 个核心命令

---

## 2. 核心设计决策

### 2. 1 生命周期

| SDD Phase | 执行模式 | 执行者 |
|-----------|----------|--------|
| Phase 1: Setup | 串行 | Team Lead |
| Phase 2: Foundational | 串行 | Team Lead |
| Phase 3+: User Stories | 并行（如多个故事） | Team Members |
| Phase N: Polish | 串行 | Team Lead |

### 2. 2 并行决策规则

```
IF user_stories.count >= 2 AND stories_have_parallel_tasks:
    spawn_parallel_execution()
ELSE:
    execute_sequentially()
```

### 2. 3 Team 架构

```
Team Name: sdd-{feature-id}
Team Lead: 当前 Claude Code Session
Team Members: 动态派生，执行完成后销毁
```

### 2. 4 状态管理

- **存储位置**: `.specify/team-config.json`
- **任务状态**: tasks.md 中的 checkbox (`- [ ]` → `- [X]` 或 `[-]` 表示失败)
- **同步机制**: Git force-with-lease

---

## 3. 命令规范

### 3. 1 /speckit.implement

**扩展行为**:

```
1. 执行 Phase 1-2（Setup + Foundational）
   → Team Lead 串行执行

2. 分析 Phase 3+ 的并行机会
   → 检测多个用户故事是否有 [P] 标记任务

3. 并行执行决策
   ├── stories >= 2: 派生 Team Members 并行执行
   └── stories <= 1: 串行执行

4. 可选参数
   ├── --serial: 强制完全串行
   └── --parallel: 强制启用并行（即使只有 1 个故事）
```

### 3. 2 保持不变的命令

| 命令 | 说明 |
|------|------|
| `/speckit.specify` | 创建规范（不变） |
| `/speckit.plan` | 创建计划（不变） |
| `/speckit.tasks` | 生成任务（不变） |

---

## 4. 并行执行架构

### 4. 1 Team Lead 职责

```
Team Lead:
├── 1. 读取 tasks.md，分析任务图
├── 2. 执行 Phase 1-2（Setup + Foundational）
├── 3. 识别可并行的用户故事
├── 4. 派生 Team Members（每个故事 1 个 Member）
├── 5. 分配任务给各 Member
├── 6. 监控进度
├── 7. 处理失败（重试或标记跳过）
├── 8. Member 完成后执行 Phase N (Polish)
└── 9. 清理 Team Members
```

### 4. 2 Team Member 职责

```
Team Member:
├── 1. 接收任务分配（task list）
├── 2. 按顺序执行分配的任务
│   ├── 遵循 TDD：测试任务先于实现任务
│   └── 遵守 [P] 标记的并行规则
├── 3. 每次完成任务后更新 tasks.md
├── 4. 向 Team Lead 报告进度
└── 5. 所有任务完成后销毁
```

### 4. 3 任务分配策略

```
分配规则:
├── 每个用户故事分配给 1 个 Team Member
├── 每个 Member 至少分配 3 个任务（否则不派生）
└── 任务分配写入 .specify/team-config.json
```

### 4. 4 派生条件

```
派生阈值: 每个故事至少 3 个任务
派生数量: min(story_count, 4)  // 最多 4 个并行

示例:
├── US1(6), US2(6), US3(6) → 3 Members
├── US1(6), US2(2)         → 2 Members（US2 合并或跳过）
└── US1(6)                 → 0 Members（串行执行）
```

---

## 5. 通信协议

### 5. 1 Team Lead → Member

```json
{
  "type": "assign",
  "member_id": "member-us1",
  "tasks": ["T010", "T011", "T012"],
  "feature_dir": "/path/to/specs/001-feature"
}
```

### 5. 2 Member → Team Lead

```json
{
  "type": "progress",
  "task_id": "T010",
  "status": "completed",
  "error": null
}
```

```json
{
  "type": "complete",
  "member_id": "member-us1",
  "completed_all": true
}
```

---

## 6. 状态管理

### 6. 1 team-config.json 结构

```json
{
  "team_name": "sdd-001-photo-album",
  "feature_dir": "/path/to/specs/001-feature",
  "created_at": "2026-04-01T10:00:00Z",
  "status": "active",
  "members": {
    "member-us1": {
      "story": "US1",
      "tasks": ["T010", "T011", "T012"],
      "status": "running"
    },
    "member-us2": {
      "story": "US2",
      "tasks": ["T016", "T017", "T018"],
      "status": "running"
    }
  }
}
```

### 6. 2 任务状态标记

```
- [ ] T010  // 未开始
- [X] T010  // 已完成
- [-] T010  // 已失败（跳过）
- [R] T010  // 正在执行
```

### 6. 3 Git force-with-lease 同步

```
1. Member 完成 T010
2. fetch origin tasks.md
3. rebase local changes
4. Update checkbox: - [ ] → - [X]
5. git add + commit + push --force-with-lease

如果 push 失败（他人更新）:
→ 重新 fetch + rebase + push
```

---

## 7. 错误处理

### 7. 1 单任务失败

```
处理流程:
1. Member 报告任务失败
2. Team Lead 重试该任务（最多 2 次）
3. 仍失败 → 标记为 [-]，继续其他任务
4. 记录失败原因到 tasks.md 注释
```

### 7. 2 Member 无响应

```
处理流程:
1. Team Lead 检测 Member 无响应（超时 5 分钟）
2. Team Lead 重新派生新 Member
3. 新 Member 从上一个成功的 checkpoint 继续
4. 如果无 checkpoint → 该故事标记为失败
```

### 7. 3 多个 Member 失败

```
处理流程:
1. 超过 50% Member 失败
2. Team Lead 终止并行执行
3. 切换为串行模式
4. Team Lead 继续执行剩余任务
```

### 7. 4 无自动回滚

```
原则: 不自动回滚已完成的工作

理由:
├── 已完成的工作可能是有效的
├── 回滚可能引入更多问题
└── 人工 Review 可决定如何处理
```

---

## 8. 执行流程

### 8. 1 完整流程图

```
/speckit.implement
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 1: Setup                      │
│ Team Lead 执行 T001-T003             │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 2: Foundational               │
│ Team Lead 执行 T004-T009             │
│ (blocking - 所有故事的依赖)          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 分析并行机会                         │
│ 读取 tasks.md                       │
│ 检测 [P] 标记和故事数量              │
└─────────────────────────────────────┘
    │
    ▼
    ├─ stories < 2 ──────────────────────→ 串行执行所有故事
    │
    └─ stories >= 2 ──────────────────────→ 派生 Team Members
                                              │
                          ┌────────────────────┼────────────────────┐
                          ▼                    ▼                    ▼
                   ┌──────────┐        ┌──────────┐        ┌──────────┐
                   │ Member-1 │        │ Member-2 │        │ Member-3 │
                   │ 执行 US1  │        │ 执行 US2  │        │ 执行 US3  │
                   │ T010-T015│        │ T016-T021│        │ T022-T027│
                   └──────────┘        └──────────┘        └──────────┘
                          │                    │                    │
                          └────────────────────┼────────────────────┘
                                               ▼
                          ┌─────────────────────────────────────┐
                          │  Phase N: Polish                    │
                          │  Team Lead 执行最终任务              │
                          │  清理 Team Members                   │
                          └─────────────────────────────────────┘
                                               │
                          ┌────────────────────┴────────────────────┐
                          ▼                                         ▼
                    所有成功                                  有失败/部分
                    任务完成                                 继续处理
```

### 8. 2 Team Member 执行循环

```
FOR each task in assigned_tasks:
    1. 标记为 [R] (running)
    2. 执行任务
    3. IF 成功:
           更新为 [X] (completed)
           push tasks.md
       ELSE:
           重试 (最多 2 次)
           IF 仍失败:
               更新为 [-] (failed)
               继续下一任务
    4. 报告进度给 Team Lead

END FOR

报告 "completed_all: true" 给 Team Lead
```

---

## 9. 实现要点

### 9. 1 Team 配置存储

```python
# 位置: .specify/team-config.json
# Team Lead 创建，任务完成后删除
```

### 9. 2 派生阈值

```python
MIN_TASKS_PER_MEMBER = 3  # 最少任务数
MAX_PARALLEL_MEMBERS = 4  # 最多并行数
```

### 9. 3 无响应检测

```python
MEMBER_TIMEOUT_MINUTES = 5  # Member 无响应超时
CHECK_INTERVAL_SECONDS = 30  # 检查间隔
```

---

## 10. 风险与限制

### 10. 1 当前限制

| 限制 | 说明 |
|------|------|
| Session 稳定性 | Session 崩溃后无法恢复 |
| 最多 4 个并行 | 超过后并行收益递减 |
| 共享 tasks.md | 需要 Git force-with-lease 同步 |

### 10. 2 不适用场景

- 单个用户故事（无并行机会）
- 任务总数少于 6 个（派生开销大于收益）
- Session 可能中断的场景（建议使用 --serial）

---

## 11. 验收标准

### 11. 1 功能验收

- [ ] Phase 1-2 由 Team Lead 串行执行
- [ ] 多个用户故事时自动派生 Team Members
- [ ] 单个用户故事时串行执行
- [ ] Team Members 执行分配的任务
- [ ] 任务状态正确更新到 tasks.md
- [ ] 失败任务标记为 [-]
- [ ] 支持 --serial 和 --parallel 参数

### 11. 2 质量验收

- [ ] 不自动回滚已完成的任务
- [ ] Member 无响应时有重试机制
- [ ] Team config 在任务完成后清理
- [ ] 不引入新的独立命令
