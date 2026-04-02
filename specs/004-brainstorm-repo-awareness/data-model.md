# Data Model: Brainstorm仓库认知增强

## Entities

### 1. 认知确认记录 (AwarenessConfirmation)

| Field | Type | Description |
|-------|------|-------------|
| userId | string | 用户标识符 |
| confirmedAt | timestamp | 最后确认时间 |
| skipUsed | boolean | 是否使用了跳过选项 |
| modeSelected | enum | "full" 或 "quick" |
| projectPath | string | 项目路径 |

### 2. 仓库概览信息 (RepositoryOverview)

| Field | Type | Description |
|-------|------|-------------|
| name | string | 项目名称 |
| description | string | 项目描述（来自README） |
| techStack | array[string] | 检测到的技术栈 |
| architecture | string | 架构描述（如果有文档） |
| dirStructure | tree | 目录结构摘要 |
| docPaths | array[string] | 可用文档路径 |

### 3. 提案元数据 (ProposalMetadata)

| Field | Type | Description |
|-------|------|-------------|
| branchNumber | string | 分支编号 如 "004" |
| shortName | string | 短名称 如 "brainstorm-repo-awareness" |
| isProposal | boolean | 固定为 true |
| awarenessCompleted | boolean | 认知阶段是否完成 |
| createdAt | timestamp | 创建时间 |

---

## State Transitions

```
[Initial] --> [Awareness Phase] --> [Skip?] --> [Confirmed/Skipped]
                                                      |
                                                      v
                                              [Proposal Generation]
```

---

## Validation Rules

- `skipUsed == true` 时需要验证用户历史确认记录
- `modeSelected` 只能是 "full" 或 "quick"
- `awarenessCompleted` 为 true 才能进入提案生成
