# Contract: Brainstorm命令仓库认知接口

## 1. 命令接口

### 新增参数

| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| `--mode` | enum | 否 | full | 认知模式：full=完整，quick=快速 |
| `--skip-awareness` | flag | 否 | false | 跳过认知阶段（需历史确认） |

### 行为契约

1. **--mode full**: 展示完整仓库信息（架构、技术栈、目录结构、所有文档）
2. **--mode quick**: 仅展示核心信息（项目名、描述、技术栈）
3. **--skip-awareness**: 仅在用户有历史确认记录时有效，否则提示需要完成认知

---

## 2. 输出契约

### Spec文件名格式

```
proposal-{branch-number}-{short-name}-spec.md
```

**Example**: `proposal-004-brainstorm-repo-awareness-spec.md`

### Spec文件Status字段

```markdown
**Status**: Proposal
```

---

## 3. 状态文件

### 存储位置

`.specify/awareness-state.json`

### Schema

```json
{
  "users": {
    "<user-id>": {
      "lastConfirmed": "<ISO-8601>",
      "skipCount": <number>,
      "preferredMode": "full|quick"
    }
  }
}
```
